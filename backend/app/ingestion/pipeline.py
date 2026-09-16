from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from qdrant_client.models import PointStruct

from backend.app.database.mongodb import (
    documents_collection,
    document_chunks_collection,
)

from backend.app.ingestion.embeddings import get_embedding_model
from backend.app.ingestion.pdf_loader import load_pdf
from backend.app.ingestion.qdrant_client import (
    COLLECTION_NAME,
    get_qdrant_client,
)
from backend.app.ingestion.text_splitter import split_documents


def generate_document_id():
    last_document = documents_collection.find_one(
        sort=[("document_id", -1)]
    )

    if not last_document:
        return "DOC-001"

    last_id = last_document["document_id"]

    number = int(last_id.split("-")[1])

    return f"DOC-{number + 1:03d}"


def ingest_pdf(
    file_path: str,
    title: str | None = None,
    uploaded_by: str = "SYSTEM",
):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    print(f"Starting ingestion: {path.name}")

    # 1. Load PDF
    documents = load_pdf(str(path))

    print(f"Loaded {len(documents)} pages.")

    # 2. Split into chunks
    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # 3. Generate document ID
    document_id = generate_document_id()

    # 4. Create document metadata
    now = datetime.now(timezone.utc)

    document = {
        "document_id": document_id,
        "filename": path.name,
        "title": title or path.stem,
        "file_type": "pdf",
        "source": "internal",
        "uploaded_by": uploaded_by,
        "status": "processing",
        "created_at": now,
        "updated_at": now,
    }

    documents_collection.insert_one(document)

    qdrant_client = get_qdrant_client()
    qdrant_points = []

    try:
        embedding_model = get_embedding_model()

        for chunk_index, chunk in enumerate(chunks):
            vector = embedding_model.embed_query(chunk.page_content)
            qdrant_point_id = str(uuid4())
            chunk_result = document_chunks_collection.insert_one(
                {
                    "document_id": document_id,
                    "text": chunk.page_content,
                    "source": chunk.metadata.get("source"),
                    "page": chunk.metadata.get("page"),
                    "chunk_index": chunk_index,
                    "qdrant_point_id": qdrant_point_id,
                    "created_at": now,
                }
            )
            qdrant_points.append(
                PointStruct(
                    id=qdrant_point_id,
                    vector=vector,
                    payload={
                        "text": chunk.page_content,
                        "source": chunk.metadata.get("source"),
                        "page": chunk.metadata.get("page"),
                        "document_id": document_id,
                        "chunk_id": str(chunk_result.inserted_id),
                        "chunk_index": chunk_index,
                    },
                )
            )

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=qdrant_points,
        )

        documents_collection.update_one(
            {"document_id": document_id},
            {
                "$set": {
                    "status": "processed",
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
    except Exception:
        document_chunks_collection.delete_many(
            {"document_id": document_id}
        )
        documents_collection.update_one(
            {"document_id": document_id},
            {
                "$set": {
                    "status": "failed",
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        raise

    print(
        f"Successfully stored {len(qdrant_points)} "
        "vectors in Qdrant."
    )

    return {
        "document_id": document_id,
        "filename": path.name,
        "pages": len(documents),
        "chunks": len(chunks),
        "status": "processed",
    }
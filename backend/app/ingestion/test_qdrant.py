from uuid import uuid4

from backend.app.ingestion.pdf_loader import load_pdf
from backend.app.ingestion.text_splitter import split_documents
from backend.app.ingestion.embeddings import get_embedding_model
from backend.app.ingestion.qdrant_client import (
    get_qdrant_client,
    COLLECTION_NAME,
)
from qdrant_client.models import PointStruct


PDF_PATH = "backend/uploads/random_test.pdf"


documents = load_pdf(PDF_PATH)

chunks = split_documents(documents)

embedding_model = get_embedding_model()

client = get_qdrant_client()


chunk = chunks[0]

vector = embedding_model.embed_query(
    chunk.page_content
)


point = PointStruct(
    id=str(uuid4()),
    vector=vector,
    payload={
        "text": chunk.page_content,
        "source": chunk.metadata.get("source"),
        "page": chunk.metadata.get("page"),
    },
)


client.upsert(
    collection_name=COLLECTION_NAME,
    points=[point],
)


print("Chunk successfully stored in Qdrant.")
print("Source:", chunk.metadata.get("source"))
print("Page:", chunk.metadata.get("page"))
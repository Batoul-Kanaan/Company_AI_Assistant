from bson import ObjectId

from backend.app.database.document_chunks import (
    create_document_chunk,
    get_document_chunk,
    get_chunks_by_document,
    update_document_chunk,
    delete_document_chunk,
)


chunk_data = {
    "document_id": "DOC-TEST-001",
    "text": "Employees may work remotely according to company guidelines.",
    "source": "test_policy.pdf",
    "page": 0,
    "chunk_index": 0,
    "qdrant_point_id": "test-qdrant-point-001",
}


print("=== CREATE ===")

chunk = create_document_chunk(chunk_data)

print(chunk)

chunk_id = chunk["_id"]


print("\n=== GET ONE ===")

chunk = get_document_chunk(chunk_id)

print(chunk)


print("\n=== GET BY DOCUMENT ===")

chunks = get_chunks_by_document(
    "DOC-TEST-001"
)

print(f"Total chunks: {len(chunks)}")


print("\n=== UPDATE ===")

updated_chunk = update_document_chunk(
    chunk_id,
    {
        "text": "Updated chunk text."
    },
)

print(updated_chunk)


print("\n=== DELETE ===")

deleted = delete_document_chunk(
    chunk_id
)

print("Deleted:", deleted)
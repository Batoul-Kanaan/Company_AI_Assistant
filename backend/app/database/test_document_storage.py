from bson import ObjectId

from backend.app.database.mongodb import (
    documents_collection,
    document_chunks_collection,
)


# 1. Create a document record
document = {
    "filename": "random_test.pdf",
    "file_path": "backend/uploads/random_test.pdf",
    "document_type": "pdf",
}


document_result = documents_collection.insert_one(document)

document_id = document_result.inserted_id

print("Document inserted successfully!")
print("Document ID:", document_id)


# 2. Create a chunk linked to the document
chunk = {
    "document_id": str(document_id),
    "text": "This is a test document chunk.",
    "source": "backend/uploads/random_test.pdf",
    "page": 0,
    "chunk_index": 0,
    "qdrant_point_id": "test-qdrant-point",
}


chunk_result = document_chunks_collection.insert_one(chunk)

print("\nChunk inserted successfully!")
print("Chunk ID:", chunk_result.inserted_id)
from datetime import datetime, timezone

from backend.app.database.mongodb import database


document_chunks_collection = database["document_chunks"]


def create_document_chunk(chunk_data: dict):
    now = datetime.now(timezone.utc)

    chunk = {
        **chunk_data,
        "created_at": now,
    }

    result = document_chunks_collection.insert_one(chunk)

    return document_chunks_collection.find_one(
        {"_id": result.inserted_id}
    )


def get_document_chunk(chunk_id):
    return document_chunks_collection.find_one(
        {"_id": chunk_id}
    )


def get_chunks_by_document(document_id: str):
    return list(
        document_chunks_collection.find(
            {"document_id": document_id}
        ).sort("chunk_index", 1)
    )


def update_document_chunk(
    chunk_id,
    update_data: dict,
):
    result = document_chunks_collection.update_one(
        {"_id": chunk_id},
        {
            "$set": update_data,
        },
    )

    if result.matched_count == 0:
        return None

    return get_document_chunk(chunk_id)


def delete_document_chunk(chunk_id):
    result = document_chunks_collection.delete_one(
        {"_id": chunk_id}
    )

    return result.deleted_count > 0
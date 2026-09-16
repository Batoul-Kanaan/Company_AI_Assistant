from datetime import datetime, timezone

from backend.app.database.mongodb import database


documents_collection = database["documents"]


def create_document(document_data: dict):
    now = datetime.now(timezone.utc)

    document = {
        **document_data,
        "created_at": now,
        "updated_at": now,
    }

    result = documents_collection.insert_one(document)

    return documents_collection.find_one(
        {"_id": result.inserted_id}
    )


def get_document(document_id: str):
    return documents_collection.find_one(
        {"document_id": document_id}
    )


def get_all_documents():
    return list(
        documents_collection.find()
    )


def search_documents(query: dict):
    return list(
        documents_collection.find(query)
    )


def update_document(
    document_id: str,
    update_data: dict,
):
    update_data["updated_at"] = datetime.now(timezone.utc)

    result = documents_collection.update_one(
        {"document_id": document_id},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        return None

    return get_document(document_id)


def delete_document(document_id: str):
    result = documents_collection.delete_one(
        {"document_id": document_id}
    )

    return result.deleted_count > 0
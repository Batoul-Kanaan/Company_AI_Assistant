from backend.app.database.mongodb import documents_collection
from backend.app.ingestion.qdrant_client import (
    COLLECTION_NAME,
    get_qdrant_client,
)
from qdrant_client.models import PointIdsList


def get_valid_document_ids():
    documents = documents_collection.find(
        {},
        {"_id": 0, "document_id": 1},
    )

    return {
        document["document_id"]
        for document in documents
        if document.get("document_id")
    }


def cleanup_orphan_points():
    client = get_qdrant_client()

    valid_document_ids = get_valid_document_ids()

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    orphan_point_ids = []

    for point in points:
        payload = point.payload or {}
        document_id = payload.get("document_id")

        if document_id not in valid_document_ids:
            orphan_point_ids.append(point.id)

    if not orphan_point_ids:
        print("No orphan points found.")
        return

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=PointIdsList(
            points=orphan_point_ids,
        ),
    )

    print(
        f"Deleted {len(orphan_point_ids)} orphan Qdrant points."
    )


if __name__ == "__main__":
    cleanup_orphan_points()
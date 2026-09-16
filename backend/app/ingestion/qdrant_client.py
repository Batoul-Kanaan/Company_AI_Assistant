import os

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333",
)
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION",
    "company_documents",
)


def get_qdrant_client():
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )


def create_collection():
    client = get_qdrant_client()

    collections = client.get_collections()

    existing_collections = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in existing_collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

        print(f"Collection '{COLLECTION_NAME}' created.")

    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")


if __name__ == "__main__":
    create_collection()
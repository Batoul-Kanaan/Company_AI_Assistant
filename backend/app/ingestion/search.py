from backend.app.ingestion.embeddings import get_embedding_model
from backend.app.ingestion.qdrant_client import (
    COLLECTION_NAME,
    get_qdrant_client,
)


def search_qdrant(
    query: str,
    limit: int = 5,
):
    embedding_model = get_embedding_model()

    query_vector = embedding_model.embed_query(query)

    client = get_qdrant_client()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True,
    )

    return results.points
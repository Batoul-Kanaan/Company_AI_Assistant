from backend.app.ingestion.search import search_qdrant


RELEVANCE_THRESHOLD = 0.20


def search_knowledge_base(
    query: str,
    limit: int = 5,
):
    results = search_qdrant(
        query=query,
        limit=limit,
    )

    knowledge_results = []

    for result in results:
        payload = result.payload or {}

        if result.score < RELEVANCE_THRESHOLD:
            continue

        knowledge_results.append(
            {
                "score": result.score,
                "document_id": payload.get("document_id"),
                "chunk_id": payload.get("chunk_id"),
                "chunk_index": payload.get("chunk_index"),
                "page": payload.get("page"),
                "text": payload.get("text"),
                "source": payload.get("source"),
            }
        )

    return knowledge_results
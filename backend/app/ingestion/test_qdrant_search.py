from backend.app.ingestion.embeddings import get_embedding_model
from backend.app.ingestion.qdrant_client import (
    get_qdrant_client,
    COLLECTION_NAME,
)


QUESTION = "How many days before vacation should I submit my request?"



embedding_model = get_embedding_model()


query_vector = embedding_model.embed_query(QUESTION)


client = get_qdrant_client()


results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=3,
).points



print(f"Question: {QUESTION}")
print(f"Number of results: {len(results)}")

for index, result in enumerate(results):
    print("\n==============================")
    print(f"RESULT {index + 1}")
    print("==============================")

    print("Score:", result.score)

    print("\nText:")
    print(result.payload.get("text"))

    print("\nSource:")
    print(result.payload.get("source"))

    print("Page:")
    print(result.payload.get("page"))
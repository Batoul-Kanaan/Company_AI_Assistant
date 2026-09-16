from backend.app.ingestion.qdrant_client import (
    get_qdrant_client,
    COLLECTION_NAME,
)


client = get_qdrant_client()

results, next_page = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=100,
    with_payload=True,
    with_vectors=False,
)

print(f"Collection: {COLLECTION_NAME}")
print(f"Number of points: {len(results)}")

for index, point in enumerate(results):
    print("\n==============================")
    print(f"POINT {index + 1}")
    print("==============================")

    print("ID:", point.id)

    print("Document ID:", point.payload.get("document_id"))

    print("Chunk ID:", point.payload.get("chunk_id"))

    print("Chunk Index:", point.payload.get("chunk_index"))

    print("Source:", point.payload.get("source"))

    print("Page:", point.payload.get("page"))

    print("Text:")
    print(point.payload.get("text"))
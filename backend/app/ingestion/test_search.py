from backend.app.ingestion.search import search_qdrant


query = "What is this random test document about?"

results = search_qdrant(
    query=query,
    limit=5,
)

print("\n==============================")
print("SEARCH RESULTS")
print("==============================")

for index, result in enumerate(results, start=1):
    print(f"\nResult #{index}")
    print(f"Score: {result.score}")
    print(f"Document ID: {result.payload.get('document_id')}")
    print(f"Chunk Index: {result.payload.get('chunk_index')}")
    print(f"Page: {result.payload.get('page')}")
    print(f"Text: {result.payload.get('text')}")
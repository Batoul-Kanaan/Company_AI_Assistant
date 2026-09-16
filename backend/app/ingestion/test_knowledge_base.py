from backend.app.ingestion.knowledge_base import search_knowledge_base


query = "What is this random test document about?"

results = search_knowledge_base(
    query=query,
    limit=5,
)

print("\n==============================")
print("KNOWLEDGE BASE RESULTS")
print("==============================")

for index, result in enumerate(results, start=1):
    print(f"\nResult #{index}")
    print(f"Score: {result['score']}")
    print(f"Document ID: {result['document_id']}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Chunk Index: {result['chunk_index']}")
    print(f"Page: {result['page']}")
    print(f"Source: {result['source']}")
    print(f"Text: {result['text']}")
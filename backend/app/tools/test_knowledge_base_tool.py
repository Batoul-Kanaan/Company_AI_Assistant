from backend.app.tools.knowledge_base import search_knowledge_base


query = "What is this random test document about?"

result = search_knowledge_base.invoke({
    "query": query,
    "limit": 3,
})

print("\n==============================")
print("LANGCHAIN TOOL RESULT")
print("==============================")

for index, item in enumerate(result, start=1):
    print(f"\nResult #{index}")
    print(f"Score: {item['score']}")
    print(f"Document ID: {item['document_id']}")
    print(f"Chunk Index: {item['chunk_index']}")
    print(f"Page: {item['page']}")
    print(f"Text: {item['text']}")
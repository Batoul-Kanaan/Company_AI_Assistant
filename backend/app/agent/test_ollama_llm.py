from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)

response = llm.invoke(
    "Say hello in one short sentence."
)

print("\n==============================")
print("OLLAMA + LANGCHAIN TEST")
print("==============================")
print(response.content)
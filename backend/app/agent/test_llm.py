from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

response = llm.invoke(
    "Say hello in one short sentence."
)

print("\n==============================")
print("LLM TEST")
print("==============================")
print(response.content)
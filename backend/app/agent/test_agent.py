from backend.app.agent.agent import run_agent


result = run_agent(
    "What is the status of Paper in the random test document?"
)

print("\n==============================")
print("AGENT TEST")
print("==============================")

print("\nFINAL ANSWER:")
print(result["final_answer"])
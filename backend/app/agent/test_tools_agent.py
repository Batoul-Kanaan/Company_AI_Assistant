from backend.app.agent.agent import run_agent


TEST_CASES = [
    {
        "question": "What is the email of employee EMP-001?",
        "expected_tool": "get_employee",
    },
    {
        "question": "What is the status of ticket TCK-1002?",
        "expected_tool": "get_ticket",
    },
    {
        "question": "Show me all open tickets.",
        "expected_tool": "search_tickets",
    },
    {
        "question": "What is the status of Paper in the random test document?",
        "expected_tool": "search_knowledge_base",
    },
]


def get_tool_calls(result: dict) -> list[str]:
    tool_calls = []

    for message in result["messages"]:
        if hasattr(message, "tool_calls"):
            for tool_call in message.tool_calls:
                tool_calls.append(tool_call["name"])

    return tool_calls


if __name__ == "__main__":
    print("\n==============================")
    print("AGENT TOOL SELECTION TEST")
    print("==============================")

    passed = 0

    for index, test_case in enumerate(TEST_CASES, start=1):
        question = test_case["question"]
        expected_tool = test_case["expected_tool"]

        print(f"\nTest #{index}")
        print(f"Question: {question}")
        print(f"Expected tool: {expected_tool}")

        result = run_agent(question)

        actual_tools = get_tool_calls(result)

        print(f"Actual tools: {actual_tools}")
        print(f"Answer: {result['final_answer']}")

        if expected_tool in actual_tools:
            print("RESULT: PASS")
            passed += 1
        else:
            print("RESULT: FAIL")

    print("\n==============================")
    print(f"RESULT: {passed}/{len(TEST_CASES)} tests passed")
    print("==============================")
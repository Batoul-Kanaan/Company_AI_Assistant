from backend.app.agent.agent import run_agent


TEST_CASES = [
    {
        "question": "What is the email of employee EMP-999?",
        "expected_tool": "get_employee",
    },
    {
        "question": "What is the status of ticket TCK-9999?",
        "expected_tool": "get_ticket",
    },
    {
        "question": "Show me tickets for employee EMP-999.",
        "expected_tool": "search_tickets",
    },
    {
        "question": "What is the company's vacation policy?",
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


def answer_indicates_not_found(answer: str) -> bool:
    answer_lower = answer.lower()

    not_found_phrases = [
        "not found",
        "could not find",
        "couldn't find",
        "no information",
        "no relevant information",
        "not available",
        "does not exist",
        "doesn't exist",
        "cannot find",
        "can't find",
        "no tickets were found",
    ]

    return any(
        phrase in answer_lower
        for phrase in not_found_phrases
    )


if __name__ == "__main__":
    print("\n==============================")
    print("AGENT NOT-FOUND TEST")
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
        answer = result["final_answer"]

        tool_passed = expected_tool in actual_tools
        answer_passed = answer_indicates_not_found(answer)

        print(f"Actual tools: {actual_tools}")
        print(f"Answer: {answer}")

        if tool_passed and answer_passed:
            print("RESULT: PASS")
            passed += 1
        else:
            print("RESULT: FAIL")

            if not tool_passed:
                print("Reason: Expected tool was not used.")

            if not answer_passed:
                print("Reason: Agent did not clearly indicate that information was not found.")

    print("\n==============================")
    print(f"RESULT: {passed}/{len(TEST_CASES)} tests passed")
    print("==============================")
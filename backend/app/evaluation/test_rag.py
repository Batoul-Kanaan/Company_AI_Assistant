import sys

from backend.app.agent.agent import run_agent
from backend.app.ingestion.knowledge_base import search_knowledge_base


NOT_FOUND_MESSAGE = (
    "The requested information was not found "
    "in the available company data."
)


TEST_CASES = [
    {
        "name": "Paper status",
        "question": "What is the status of Paper in the random test document?",
        "expected_document_id": "DOC-005",
        "expected_chunk_index": 0,
        "expected_facts": ["Paper", "OK"],
        "should_find_information": True,
    },
    {
        "name": "Coffee status",
        "question": "What is the status of Coffee in the random test document?",
        "expected_document_id": "DOC-005",
        "expected_chunk_index": 0,
        "expected_facts": ["Coffee", "Pending"],
        "should_find_information": True,
    },
    {
        "name": "Missing company policy",
        "question": "What is the company's vacation policy?",
        "expected_document_id": None,
        "expected_chunk_index": None,
        "expected_facts": [],
        "should_find_information": False,
    },
]


def evaluate_retrieval(test_case: dict):
    results = search_knowledge_base(
        query=test_case["question"],
        limit=5,
    )

    if not test_case["should_find_information"]:
        return {
            "passed": len(results) == 0,
            "results_count": len(results),
            "expected_document_id": None,
            "expected_chunk_index": None,
        }

    matching_results = [
        result
        for result in results
        if (
            result.get("document_id")
            == test_case["expected_document_id"]
            and result.get("chunk_index")
            == test_case["expected_chunk_index"]
        )
    ]

    facts_found = all(
        any(
            fact.lower() in result.get("text", "").lower()
            for result in matching_results
        )
        for fact in test_case["expected_facts"]
    )

    passed = bool(matching_results) and facts_found

    return {
        "passed": passed,
        "results_count": len(results),
        "expected_document_id": test_case["expected_document_id"],
        "expected_chunk_index": test_case["expected_chunk_index"],
    }


def evaluate_answer(test_case: dict):
    result = run_agent(test_case["question"])

    final_answer = result["final_answer"]

    if test_case["should_find_information"]:
        passed = all(
            fact.lower() in final_answer.lower()
            for fact in test_case["expected_facts"]
        )
    else:
        passed = final_answer == NOT_FOUND_MESSAGE

    return {
        "passed": passed,
        "actual_answer": final_answer,
    }


def evaluate_test_case(test_case: dict):
    retrieval_result = evaluate_retrieval(test_case)
    answer_result = evaluate_answer(test_case)

    return {
        "name": test_case["name"],
        "question": test_case["question"],
        "retrieval_passed": retrieval_result["passed"],
        "answer_passed": answer_result["passed"],
        "retrieval_results_count": retrieval_result["results_count"],
        "expected_document_id": retrieval_result[
            "expected_document_id"
        ],
        "expected_chunk_index": retrieval_result[
            "expected_chunk_index"
        ],
        "actual_answer": answer_result["actual_answer"],
        "passed": (
            retrieval_result["passed"]
            and answer_result["passed"]
        ),
    }


def run_evaluation():
    results = []

    for test_case in TEST_CASES:
        result = evaluate_test_case(test_case)
        results.append(result)

    return results


def print_result(index: int, result: dict):
    status = "PASS" if result["passed"] else "FAIL"

    print(f"\nTest #{index}: {status}")
    print(f"Name: {result['name']}")
    print(f"Question: {result['question']}")

    print("\nRetrieval:")
    print(
        f"  Expected document: "
        f"{result['expected_document_id']}"
    )
    print(
        f"  Expected chunk: "
        f"{result['expected_chunk_index']}"
    )
    print(
        f"  Results returned: "
        f"{result['retrieval_results_count']}"
    )
    print(
        f"  Retrieval: "
        f"{'PASS' if result['retrieval_passed'] else 'FAIL'}"
    )

    print("\nAnswer:")
    print(f"  {result['actual_answer']}")
    print(
        f"  Answer correctness: "
        f"{'PASS' if result['answer_passed'] else 'FAIL'}"
    )


if __name__ == "__main__":
    results = run_evaluation()

    print("\n==============================")
    print("RAG EVALUATION")
    print("==============================")

    total = len(results)

    passed_count = sum(
        result["passed"]
        for result in results
    )

    retrieval_passed_count = sum(
        result["retrieval_passed"]
        for result in results
    )

    answer_passed_count = sum(
        result["answer_passed"]
        for result in results
    )

    for index, result in enumerate(results, start=1):
        print_result(index, result)

    print("\n==============================")
    print(
        f"OVERALL: "
        f"{passed_count}/{total} tests passed"
    )
    print(
        f"RETRIEVAL: "
        f"{retrieval_passed_count}/{total} passed"
    )
    print(
        f"ANSWER: "
        f"{answer_passed_count}/{total} passed"
    )
    print("==============================")

    if passed_count != total:
        sys.exit(1)
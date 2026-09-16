import uuid

from langchain_core.messages import ToolMessage

from backend.app.agent.agent import run_agent
from backend.app.database.tickets import (
    get_ticket,
    delete_ticket,
)


def get_tool_calls(result: dict) -> list[str]:
    tool_calls = []

    for message in result["messages"]:
        if hasattr(message, "tool_calls"):
            for tool_call in message.tool_calls:
                tool_calls.append(tool_call["name"])

    return tool_calls


def get_tool_result(result: dict, tool_name: str):
    for message in result["messages"]:
        if (
            isinstance(message, ToolMessage)
            and message.name == tool_name
        ):
            return message.content

    return None


if __name__ == "__main__":
    ticket_id = f"TKT-AGENT-{uuid.uuid4().hex[:8].upper()}"

    print("\n==============================")
    print("AGENT MUTATION TOOLS TEST")
    print("==============================")

    # --------------------------------------------------
    # TEST 1: CREATE TICKET
    # --------------------------------------------------

    create_question = (
        f"Create a support ticket with ticket ID {ticket_id}. "
        "Employee EMP-001 has a laptop running very slowly. "
        "The category is IT and the priority is high. "
        "Assign it to EMP-002."
    )

    print("\nTest #1: CREATE TICKET")
    print(f"Question: {create_question}")

    create_result = run_agent(create_question)

    create_tools = get_tool_calls(create_result)
    create_tool_result = get_tool_result(
        create_result,
        "create_ticket",
    )

    print(f"Actual tools: {create_tools}")
    print(f"Tool result: {create_tool_result}")
    print(f"Answer: {create_result['final_answer']}")

    created_ticket = get_ticket(ticket_id)

    if (
        "create_ticket" in create_tools
        and created_ticket
        and created_ticket.get("ticket_id") == ticket_id
        and created_ticket.get("employee_id") == "EMP-001"
        and created_ticket.get("category") == "IT"
        and created_ticket.get("priority") == "high"
        and created_ticket.get("assigned_to") == "EMP-002"
    ):
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL")

    # --------------------------------------------------
    # TEST 2: UPDATE TICKET
    # --------------------------------------------------

    update_question = (
        f"Update ticket {ticket_id} and change its priority to low."
    )

    print("\nTest #2: UPDATE TICKET")
    print(f"Question: {update_question}")

    update_result = run_agent(update_question)

    update_tools = get_tool_calls(update_result)
    update_tool_result = get_tool_result(
        update_result,
        "update_ticket",
    )

    print(f"Actual tools: {update_tools}")
    print(f"Tool result: {update_tool_result}")
    print(f"Answer: {update_result['final_answer']}")

    updated_ticket = get_ticket(ticket_id)

    if (
        "update_ticket" in update_tools
        and updated_ticket
        and updated_ticket.get("ticket_id") == ticket_id
        and updated_ticket.get("priority") == "low"
    ):
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL")

    # --------------------------------------------------
    # CLEANUP
    # --------------------------------------------------

    print("\nCleaning up test ticket...")

    if get_ticket(ticket_id):
        delete_ticket(ticket_id)
        print("Test ticket deleted.")

    print("\n==============================")
    print("MUTATION TEST COMPLETED")
    print("==============================")
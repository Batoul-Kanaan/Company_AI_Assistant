from typing import Annotated, Any

from langchain.tools import tool
from pydantic import BeforeValidator

from backend.app.database.employees import (
    get_employee as get_employee_from_database,
)

from backend.app.database.tickets import (
    get_ticket as get_ticket_from_database,
    search_tickets as search_tickets_from_database,
    create_ticket as create_ticket_in_database,
    update_ticket as update_ticket_in_database,
)

from backend.app.models.ticket import (
    TicketPriority,
    TicketStatus,
)


VALID_PRIORITIES = {
    priority.value
    for priority in TicketPriority
}

VALID_STATUSES = {
    status.value
    for status in TicketStatus
}


def _empty_object_to_none(value: Any) -> Any:
    """
    Convert an empty object produced by some LLM tool calls
    into None for optional string filters.
    """

    if value == {}:
        return None

    return value


OptionalFilter = Annotated[
    str | None,
    BeforeValidator(_empty_object_to_none),
]


@tool
def get_ticket(ticket_id: str) -> dict:
    """
    Get a support ticket from the company's ticket database.

    Use this tool when you need information about a specific
    support ticket.

    Args:
        ticket_id: The unique ticket ID, for example TCK-1002.

    Returns:
        The ticket information if found, otherwise an empty dictionary.
    """
    ticket = get_ticket_from_database(ticket_id)

    if not ticket:
        return {}

    ticket["_id"] = str(ticket["_id"])

    return ticket


@tool
def search_tickets(
    status: OptionalFilter = None,
    priority: OptionalFilter = None,
    category: OptionalFilter = None,
    employee_id: OptionalFilter = None,
) -> list[dict]:
    """
    Search the company's support tickets using optional filters.

    Use this tool when you need to find one or more tickets
    matching specific criteria.

    Args:
        status: Filter by ticket status.
        priority: Filter by ticket priority.
        category: Filter by ticket category.
        employee_id: Filter by the employee who created the ticket.

    Returns:
        A list of matching tickets.
    """
    if status is not None and status not in VALID_STATUSES:
        return []

    if priority is not None and priority not in VALID_PRIORITIES:
        return []

    query = {}

    if status:
        query["status"] = status

    if priority:
        query["priority"] = priority

    if category:
        query["category"] = category

    if employee_id:
        query["employee_id"] = employee_id

    tickets = search_tickets_from_database(query)

    for ticket in tickets:
        ticket["_id"] = str(ticket["_id"])

    return tickets


@tool
def create_ticket(
    ticket_id: str,
    employee_id: str,
    title: str,
    description: str,
    category: str,
    priority: str = "medium",
    status: str = "open",
    assigned_to: str | None = None,
) -> dict:
    """
    Create a new support ticket in the company's ticket database.

    Use this tool when a new support ticket needs to be created.

    Args:
        ticket_id: Unique ticket ID, for example TKT-1003.
        employee_id: Employee ID of the employee creating the ticket.
        title: Short title describing the issue.
        description: Detailed description of the issue.
        category: Ticket category, for example IT.
        priority: Ticket priority.
        status: Initial ticket status.
        assigned_to: Optional employee ID of the assigned support employee.

    Returns:
        The newly created ticket, or an error message if validation fails.
    """
    existing_ticket = get_ticket_from_database(ticket_id)

    if existing_ticket:
        return {
            "error": "Ticket already exists",
            "ticket_id": ticket_id,
        }

    if priority not in VALID_PRIORITIES:
        return {
            "error": "Invalid ticket priority",
            "priority": priority,
        }

    if status not in VALID_STATUSES:
        return {
            "error": "Invalid ticket status",
            "status": status,
        }

    employee = get_employee_from_database(employee_id)

    if not employee:
        return {
            "error": "Employee not found",
            "employee_id": employee_id,
        }

    if assigned_to:
        assigned_employee = get_employee_from_database(assigned_to)

        if not assigned_employee:
            return {
                "error": "Assigned employee not found",
                "assigned_to": assigned_to,
            }

    ticket_data = {
        "ticket_id": ticket_id,
        "employee_id": employee_id,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }

    ticket = create_ticket_in_database(ticket_data)

    if not ticket:
        return {
            "error": "Failed to create ticket",
            "ticket_id": ticket_id,
        }

    ticket["_id"] = str(ticket["_id"])

    return ticket


@tool
def update_ticket(
    ticket_id: str,
    title: str | None = None,
    description: str | None = None,
    category: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    assigned_to: str | None = None,
    clear_assignment: bool = False,
) -> dict:
    """
    Update an existing support ticket.

    Use this tool when information on an existing ticket
    needs to be changed.

    Args:
        ticket_id: The unique ticket ID.
        title: New ticket title.
        description: New ticket description.
        category: New ticket category.
        priority: New ticket priority.
        status: New ticket status.
        assigned_to: New assigned employee ID.
        clear_assignment: Remove the currently assigned employee.

    Returns:
        The updated ticket, or an error if the ticket does not exist.
    """
    existing_ticket = get_ticket_from_database(ticket_id)

    if not existing_ticket:
        return {
            "error": "Ticket not found",
            "ticket_id": ticket_id,
        }

    if clear_assignment and assigned_to:
        return {
            "error": (
                "Cannot set assigned_to and clear_assignment "
                "at the same time"
            ),
            "ticket_id": ticket_id,
        }

    if priority is not None and priority not in VALID_PRIORITIES:
        return {
            "error": "Invalid ticket priority",
            "priority": priority,
        }

    if status is not None and status not in VALID_STATUSES:
        return {
            "error": "Invalid ticket status",
            "status": status,
        }

    if assigned_to:
        assigned_employee = get_employee_from_database(assigned_to)

        if not assigned_employee:
            return {
                "error": "Assigned employee not found",
                "assigned_to": assigned_to,
            }

    update_data = {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
    }

    if status is not None:
        update_data["status"] = status

    if assigned_to is not None:
        update_data["assigned_to"] = assigned_to

    if clear_assignment:
        update_data["assigned_to"] = None

    update_data = {
        key: value
        for key, value in update_data.items()
        if value is not None
    }

    if clear_assignment:
        update_data["assigned_to"] = None

    if not update_data:
        return {
            "error": "No fields provided for update",
            "ticket_id": ticket_id,
        }

    updated_ticket = update_ticket_in_database(
        ticket_id,
        update_data,
    )

    if not updated_ticket:
        return {
            "error": "Failed to update ticket",
            "ticket_id": ticket_id,
        }

    updated_ticket["_id"] = str(updated_ticket["_id"])

    return updated_ticket
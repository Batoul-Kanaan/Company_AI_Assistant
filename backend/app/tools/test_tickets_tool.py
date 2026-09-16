import uuid

from backend.app.tools.tickets import (
    get_ticket,
    search_tickets,
    create_ticket,
    update_ticket,
)
from backend.app.database.tickets import (
    delete_ticket,
)


def test_get_ticket_found():
    result = get_ticket.invoke(
        {"ticket_id": "TCK-1002"}
    )

    assert result["ticket_id"] == "TCK-1002"
    assert result["employee_id"] == "EMP-001"
    assert result["title"] == "Laptop issue"
    assert result["status"] == "open"


def test_get_ticket_not_found():
    result = get_ticket.invoke(
        {"ticket_id": "TKT-NOT-FOUND"}
    )

    assert result == {}


def test_search_tickets_by_status():
    results = search_tickets.invoke(
        {"status": "open"}
    )

    assert len(results) > 0
    assert all(
        ticket["status"] == "open"
        for ticket in results
    )


def test_search_tickets_by_employee():
    results = search_tickets.invoke(
        {"employee_id": "EMP-001"}
    )

    assert len(results) > 0
    assert all(
        ticket["employee_id"] == "EMP-001"
        for ticket in results
    )


def test_search_tickets_without_filters():
    results = search_tickets.invoke({})

    assert len(results) > 0


def test_create_ticket():
    ticket_id = f"TKT-TEST-{uuid.uuid4().hex[:8]}"

    try:
        result = create_ticket.invoke(
            {
                "ticket_id": ticket_id,
                "employee_id": "EMP-001",
                "title": "Tool test issue",
                "description": "Testing ticket creation tool.",
                "category": "IT",
                "priority": "low",
            }
        )

        assert result["ticket_id"] == ticket_id
        assert result["employee_id"] == "EMP-001"
        assert result["title"] == "Tool test issue"
        assert result["priority"] == "low"
        assert result["status"] == "open"

    finally:
        delete_ticket(ticket_id)


def test_create_duplicate_ticket():
    ticket_id = f"TKT-TEST-{uuid.uuid4().hex[:8]}"

    try:
        first_result = create_ticket.invoke(
            {
                "ticket_id": ticket_id,
                "employee_id": "EMP-001",
                "title": "Tool duplicate test",
                "description": "Testing duplicate ticket protection.",
                "category": "IT",
            }
        )

        assert first_result["ticket_id"] == ticket_id

        second_result = create_ticket.invoke(
            {
                "ticket_id": ticket_id,
                "employee_id": "EMP-001",
                "title": "Another issue",
                "description": "This should not be created.",
                "category": "IT",
            }
        )

        assert second_result["error"] == "Ticket already exists"
        assert second_result["ticket_id"] == ticket_id

    finally:
        delete_ticket(ticket_id)


def test_create_ticket_employee_not_found():
    ticket_id = f"TKT-TEST-{uuid.uuid4().hex[:8]}"

    result = create_ticket.invoke(
        {
            "ticket_id": ticket_id,
            "employee_id": "EMP-NOT-FOUND",
            "title": "Invalid employee test",
            "description": "Employee should not exist.",
            "category": "IT",
        }
    )

    assert result["error"] == "Employee not found"
    assert result["employee_id"] == "EMP-NOT-FOUND"


def test_create_ticket_assigned_employee_not_found():
    ticket_id = f"TKT-TEST-{uuid.uuid4().hex[:8]}"

    result = create_ticket.invoke(
        {
            "ticket_id": ticket_id,
            "employee_id": "EMP-001",
            "title": "Invalid assignment test",
            "description": "Assigned employee should not exist.",
            "category": "IT",
            "assigned_to": "EMP-NOT-FOUND",
        }
    )

    assert result["error"] == "Assigned employee not found"
    assert result["assigned_to"] == "EMP-NOT-FOUND"


def test_update_ticket():
    result = update_ticket.invoke(
        {
            "ticket_id": "TCK-1002",
            "priority": "high",
        }
    )

    assert result["ticket_id"] == "TCK-1002"
    assert result["priority"] == "high"


def test_update_ticket_not_found():
    result = update_ticket.invoke(
        {
            "ticket_id": "TKT-NOT-FOUND",
            "priority": "high",
        }
    )

    assert result["error"] == "Ticket not found"
    assert result["ticket_id"] == "TKT-NOT-FOUND"


def test_update_ticket_assigned_employee_not_found():
    result = update_ticket.invoke(
        {
            "ticket_id": "TCK-1002",
            "assigned_to": "EMP-NOT-FOUND",
        }
    )

    assert result["error"] == "Assigned employee not found"
    assert result["assigned_to"] == "EMP-NOT-FOUND"
    
def test_create_ticket_invalid_priority():
    ticket_id = f"TKT-TEST-{uuid.uuid4().hex[:8]}"

    result = create_ticket.invoke(
        {
            "ticket_id": ticket_id,
            "employee_id": "EMP-001",
            "title": "Invalid priority test",
            "description": "Testing invalid priority.",
            "category": "IT",
            "priority": "urgent",
        }
    )

    assert result["error"] == "Invalid ticket priority"
    assert result["priority"] == "urgent"


def test_create_ticket_invalid_status():
    ticket_id = f"TKT-TEST-{uuid.uuid4().hex[:8]}"

    result = create_ticket.invoke(
        {
            "ticket_id": ticket_id,
            "employee_id": "EMP-001",
            "title": "Invalid status test",
            "description": "Testing invalid status.",
            "category": "IT",
            "status": "pending",
        }
    )

    assert result["error"] == "Invalid ticket status"
    assert result["status"] == "pending"


def test_update_ticket_invalid_priority():
    result = update_ticket.invoke(
        {
            "ticket_id": "TCK-1002",
            "priority": "urgent",
        }
    )

    assert result["error"] == "Invalid ticket priority"
    assert result["priority"] == "urgent"


def test_update_ticket_invalid_status():
    result = update_ticket.invoke(
        {
            "ticket_id": "TCK-1002",
            "status": "pending",
        }
    )

    assert result["error"] == "Invalid ticket status"
    assert result["status"] == "pending"

def test_update_ticket_clear_assignment():
    result = update_ticket.invoke(
        {
            "ticket_id": "TCK-1002",
            "assigned_to": "EMP-002",
        }
    )

    assert result["ticket_id"] == "TCK-1002"
    assert result["assigned_to"] == "EMP-002"

    result = update_ticket.invoke(
        {
            "ticket_id": "TCK-1002",
            "clear_assignment": True,
        }
    )

    assert result["ticket_id"] == "TCK-1002"
    assert result["assigned_to"] is None

def test_update_ticket_assignment_conflict():
    result = update_ticket.invoke(
        {
            "ticket_id": "TCK-1002",
            "assigned_to": "EMP-002",
            "clear_assignment": True,
        }
    )

    assert result["error"] == (
        "Cannot set assigned_to and clear_assignment at the same time"
    )

if __name__ == "__main__":
    test_get_ticket_found()
    test_get_ticket_not_found()
    test_search_tickets_by_status()
    test_search_tickets_by_employee()
    test_search_tickets_without_filters()
    test_create_ticket()
    test_create_duplicate_ticket()
    test_create_ticket_employee_not_found()
    test_create_ticket_assigned_employee_not_found()
    test_update_ticket()
    test_update_ticket_not_found()
    test_update_ticket_assigned_employee_not_found()
    test_create_ticket_invalid_priority()
    test_create_ticket_invalid_status()
    test_update_ticket_invalid_priority()
    test_update_ticket_invalid_status()
    test_update_ticket_clear_assignment()
    test_update_ticket_assignment_conflict()

    print("Ticket tool tests passed successfully.")
    

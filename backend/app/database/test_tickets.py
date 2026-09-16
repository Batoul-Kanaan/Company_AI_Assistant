from backend.app.database.tickets import (
    create_ticket,
    get_ticket,
    get_all_tickets,
    search_tickets,
    update_ticket,
    delete_ticket,
)


ticket_data = {
    "ticket_id": "TKT-TEST-001",
    "employee_id": "EMP-001",
    "title": "Laptop issue",
    "description": "Laptop is not connecting to Wi-Fi",
    "category": "IT",
    "priority": "high",
    "status": "open",
    "assigned_to": "EMP-002",
}


print("=== CREATE ===")

ticket = create_ticket(ticket_data)

print(ticket)


print("\n=== GET ONE ===")

ticket = get_ticket("TKT-TEST-001")

print(ticket)


print("\n=== GET ALL ===")

tickets = get_all_tickets()

print(f"Total tickets: {len(tickets)}")


print("\n=== SEARCH ===")

tickets = search_tickets({
    "priority": "high"
})

print(f"High priority tickets: {len(tickets)}")


print("\n=== UPDATE ===")

updated_ticket = update_ticket(
    "TKT-TEST-001",
    {
        "status": "in_progress",
    },
)

print(updated_ticket)


print("\n=== DELETE ===")

deleted = delete_ticket("TKT-TEST-001")

print("Deleted:", deleted)
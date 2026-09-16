from backend.app.models.ticket import TicketCreate


ticket = TicketCreate(
    ticket_id="TKT-TEST-001",
    employee_id="EMP-001",
    title="Laptop issue",
    description="Laptop is not connecting to Wi-Fi",
    category="IT",
    priority="high",
)


print(ticket)
print("Ticket model OK")
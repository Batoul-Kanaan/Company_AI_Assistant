from pydantic import ValidationError

from backend.app.models.employee import EmployeeCreate
from backend.app.models.ticket import TicketCreate


print("=== PYDANTIC VALIDATION TEST ===")


print("\n1. Valid employee")

employee = EmployeeCreate(
    employee_id="EMP-TEST-100",
    first_name="John",
    last_name="Doe",
    email="john.doe@company.com",
    department="IT",
    role="Software Engineer",
)

print(employee)
print("PASS")


print("\n2. Invalid employee email")

try:
    EmployeeCreate(
        employee_id="EMP-TEST-101",
        first_name="John",
        last_name="Doe",
        email="invalid-email",
        department="IT",
        role="Software Engineer",
    )

    print("FAIL: Invalid email was accepted")

except ValidationError:
    print("PASS: Invalid email rejected")


print("\n3. Invalid employee status")

try:
    EmployeeCreate(
        employee_id="EMP-TEST-102",
        first_name="John",
        last_name="Doe",
        email="john2@company.com",
        department="IT",
        role="Software Engineer",
        status="banana",
    )

    print("FAIL: Invalid status was accepted")

except ValidationError:
    print("PASS: Invalid status rejected")


print("\n4. Valid ticket")

ticket = TicketCreate(
    ticket_id="TKT-TEST-100",
    employee_id="EMP-001",
    title="Laptop issue",
    description="Laptop is not connecting to Wi-Fi",
    category="IT",
    priority="high",
    status="open",
)

print(ticket)
print("PASS")


print("\n5. Invalid ticket priority")

try:
    TicketCreate(
        ticket_id="TKT-TEST-101",
        employee_id="EMP-001",
        title="Laptop issue",
        description="Laptop is not connecting to Wi-Fi",
        category="IT",
        priority="banana",
    )

    print("FAIL: Invalid priority was accepted")

except ValidationError:
    print("PASS: Invalid priority rejected")


print("\n6. Invalid ticket status")

try:
    TicketCreate(
        ticket_id="TKT-TEST-102",
        employee_id="EMP-001",
        title="Laptop issue",
        description="Laptop is not connecting to Wi-Fi",
        category="IT",
        priority="high",
        status="banana",
    )

    print("FAIL: Invalid status was accepted")

except ValidationError:
    print("PASS: Invalid status rejected")


print("\n=== VALIDATION TEST COMPLETED ===")
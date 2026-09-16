from backend.app.database.employees import (
    create_employee,
    get_employee,
    get_all_employees,
    update_employee,
    delete_employee,
)


employee_data = {
    "employee_id": "EMP-TEST-001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@company.com",
    "department": "IT",
    "role": "Software Engineer",
    "status": "active",
}


print("=== CREATE ===")

employee = create_employee(employee_data)

print(employee)


print("\n=== GET ONE ===")

employee = get_employee("EMP-TEST-001")

print(employee)


print("\n=== GET ALL ===")

employees = get_all_employees()

print(f"Total employees: {len(employees)}")


print("\n=== UPDATE ===")

updated_employee = update_employee(
    "EMP-TEST-001",
    {
        "role": "Senior Software Engineer",
    },
)

print(updated_employee)


print("\n=== DELETE ===")

deleted = delete_employee("EMP-TEST-001")

print("Deleted:", deleted)
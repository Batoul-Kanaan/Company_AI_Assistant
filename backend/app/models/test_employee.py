from backend.app.models.employee import EmployeeCreate


employee = EmployeeCreate(
    employee_id="EMP-TEST-001",
    first_name="John",
    last_name="Doe",
    email="john.doe@company.com",
    department="IT",
    role="Software Engineer",
)

print(employee)
print("Employee model OK")
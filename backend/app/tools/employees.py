from langchain.tools import tool

from backend.app.database.employees import (
    get_employee as get_employee_from_database,
    get_all_employees as get_all_employees_from_database,
)


@tool
def get_employee(employee_id: str) -> dict:
    """
    Get an employee's information from the company's employee database.

    Use this tool when you need information about a specific employee.

    Args:
        employee_id: The unique employee ID, for example EMP-001.

    Returns:
        The employee information if found, otherwise an empty dictionary.
    """
    employee = get_employee_from_database(employee_id)

    if not employee:
        return {}

    employee["_id"] = str(employee["_id"])

    return employee


@tool
def list_employees() -> list[dict]:
    """
    Get all employees from the company's employee database.

    Use this tool when the user asks for a list of employees or
    information about all employees.

    Returns:
        A list of employee records, or an empty list when none exist.
    """
    employees = get_all_employees_from_database()

    for employee in employees:
        employee["_id"] = str(employee["_id"])

    return employees
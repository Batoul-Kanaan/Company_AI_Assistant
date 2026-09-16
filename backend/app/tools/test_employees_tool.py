from backend.app.tools.employees import get_employee


def test_get_employee_found():
    result = get_employee.invoke(
        {"employee_id": "EMP-001"}
    )

    assert result["employee_id"] == "EMP-001"
    assert result["first_name"] == "John"
    assert result["last_name"] == "Smith"


def test_get_employee_not_found():
    result = get_employee.invoke(
        {"employee_id": "EMP-999"}
    )

    assert result == {}


if __name__ == "__main__":
    test_get_employee_found()
    test_get_employee_not_found()

    print("Employee tool tests passed successfully.")
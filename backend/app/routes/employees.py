from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.auth import verify_credentials

from backend.app.database.employees import (
    create_employee,
    get_employee,
    get_all_employees,
    update_employee,
    delete_employee,
)
from backend.app.models.employee import (
    EmployeeCreate,
    EmployeeUpdate,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    dependencies=[Depends(verify_credentials)],
)


def serialize_employee(employee: dict):
    if employee:
        employee["_id"] = str(employee["_id"])

    return employee


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee_route(employee: EmployeeCreate):
    existing_employee = get_employee(employee.employee_id)

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee already exists",
        )

    result = create_employee(employee.model_dump())

    return serialize_employee(result)


@router.get("/")
def get_employees():
    employees = get_all_employees()

    return [
        serialize_employee(employee)
        for employee in employees
    ]


@router.get("/{employee_id}")
def get_employee_route(employee_id: str):
    employee = get_employee(employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return serialize_employee(employee)


@router.put("/{employee_id}")
def update_employee_route(
    employee_id: str,
    employee: EmployeeUpdate,
):
    existing_employee = get_employee(employee_id)

    if not existing_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    updated_employee = update_employee(
    employee_id,
    employee.model_dump(exclude_unset=True),
)

    return serialize_employee(updated_employee)


@router.delete("/{employee_id}")
def delete_employee_route(employee_id: str):
    deleted = delete_employee(employee_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return {
        "message": "Employee deleted successfully"
    }
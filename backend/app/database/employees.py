from datetime import datetime, timezone

from backend.app.database.mongodb import database


employees_collection = database["employees"]


def create_employee(employee_data: dict):
    now = datetime.now(timezone.utc)

    employee = {
        **employee_data,
        "created_at": now,
        "updated_at": now,
    }

    result = employees_collection.insert_one(employee)

    return employees_collection.find_one(
        {"_id": result.inserted_id}
    )


def get_employee(employee_id: str):
    return employees_collection.find_one(
        {"employee_id": employee_id}
    )


def get_all_employees():
    return list(employees_collection.find())


def update_employee(employee_id: str, update_data: dict):
    update_data["updated_at"] = datetime.now(timezone.utc)

    result = employees_collection.update_one(
        {"employee_id": employee_id},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        return None

    return get_employee(employee_id)


def delete_employee(employee_id: str):
    result = employees_collection.delete_one(
        {"employee_id": employee_id}
    )

    return result.deleted_count > 0
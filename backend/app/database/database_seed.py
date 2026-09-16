import argparse
from datetime import datetime, timezone

from pymongo.errors import DuplicateKeyError

from backend.app.auth import create_user
from backend.app.database.mongodb import client, database


employees_collection = database["employees"]
policies_collection = database["policies"]
tickets_collection = database["tickets"]
users_collection = database["users"]


def seed_users():
    users = [
        {"username": "admin", "password": "admin123"},
        {"username": "alice", "password": "alice123"},
        {"username": "bob", "password": "bob123"},
    ]

    for user in users:
        try:
            create_user(user["username"], user["password"])
        except DuplicateKeyError:
            continue


def seed_employees(force: bool = False):
    employees = [
        {
            "employee_id": "EMP-1001",
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@company.com",
            "department": "Engineering",
            "role": "Senior Software Engineer",
            "status": "active",
        },
        {
            "employee_id": "EMP-1002",
            "first_name": "Bob",
            "last_name": "Williams",
            "email": "bob.williams@company.com",
            "department": "Operations",
            "role": "Operations Manager",
            "status": "active",
        },
        {
            "employee_id": "EMP-1003",
            "first_name": "Carla",
            "last_name": "Martinez",
            "email": "carla.martinez@company.com",
            "department": "Human Resources",
            "role": "HR Specialist",
            "status": "active",
        },
    ]

    if force:
        employees_collection.delete_many({})
        employees_collection.insert_many(employees)
        return

    if employees_collection.count_documents({}) == 0:
        employees_collection.insert_many(employees)


def seed_policies(force: bool = False):
    policies = [
        {
            "policy_id": "POL-2001",
            "title": "Remote Work Policy",
            "category": "HR",
            "summary": "Employees may work remotely up to three days per week with manager approval.",
            "version": "v1.2",
            "effective_date": "2025-01-15",
            "owner": "Human Resources",
        },
        {
            "policy_id": "POL-2002",
            "title": "Expense Reimbursement Policy",
            "category": "Finance",
            "summary": "Business travel and approved software purchases are reimbursable within 30 days.",
            "version": "v2.0",
            "effective_date": "2024-09-01",
            "owner": "Finance",
        },
        {
            "policy_id": "POL-2003",
            "title": "Information Security Policy",
            "category": "Security",
            "summary": "All employees must use approved devices and reports suspicious activity immediately.",
            "version": "v3.1",
            "effective_date": "2025-02-20",
            "owner": "IT Security",
        },
    ]

    if force:
        policies_collection.delete_many({})
        policies_collection.insert_many(policies)
        return

    if policies_collection.count_documents({}) == 0:
        policies_collection.insert_many(policies)


def seed_tickets(force: bool = False):
    tickets = [
        {
            "ticket_id": "TCK-3001",
            "title": "Laptop replacement request",
            "description": "Employee needs a replacement laptop after hardware failure.",
            "status": "open",
            "priority": "high",
            "employee_id": "EMP-1001",
            "department": "Engineering",
            "created_by": "alice",
        },
        {
            "ticket_id": "TCK-3002",
            "title": "Access request for new vendor portal",
            "description": "Requested access to the vendor portal for a consultant onboarding project.",
            "status": "in_progress",
            "priority": "medium",
            "employee_id": "EMP-1002",
            "department": "Operations",
            "created_by": "bob",
        },
        {
            "ticket_id": "TCK-3003",
            "title": "Payroll question",
            "description": "Employee asks for clarification on overtime adjustments in the payroll report.",
            "status": "resolved",
            "priority": "low",
            "employee_id": "EMP-1003",
            "department": "Human Resources",
            "created_by": "admin",
        },
    ]

    if force:
        tickets_collection.delete_many({})
        tickets_collection.insert_many(tickets)
        return

    if tickets_collection.count_documents({}) == 0:
        tickets_collection.insert_many(tickets)


def seed_database(force: bool = False):
    try:
        client.admin.command("ping")
    except Exception as exc:
        raise SystemExit(
            "MongoDB is not available. Start the database service and rerun the seed command."
        ) from exc

    now = datetime.now(timezone.utc)

    seed_users()
    seed_employees(force=force)
    seed_policies(force=force)
    seed_tickets(force=force)

    for collection_name in ["employees", "policies", "tickets"]:
        collection = database[collection_name]
        existing = collection.count_documents({})
        if existing > 0:
            collection.update_many(
                {},
                {"$set": {"created_at": now, "updated_at": now}},
            )

    print(
        "Database seeded successfully."
        if not force
        else "Database reset and seeded successfully."
    )


def main():
    parser = argparse.ArgumentParser(description="Seed MongoDB with demo company data.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete existing records before inserting seed data.",
    )
    args = parser.parse_args()
    seed_database(force=args.force)


if __name__ == "__main__":
    main()

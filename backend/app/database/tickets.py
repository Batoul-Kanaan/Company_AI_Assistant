from datetime import datetime, timezone

from backend.app.database.mongodb import database


tickets_collection = database["tickets"]


def create_ticket(ticket_data: dict):
    now = datetime.now(timezone.utc)

    ticket = {
        **ticket_data,
        "created_at": now,
        "updated_at": now,
    }

    result = tickets_collection.insert_one(ticket)

    return tickets_collection.find_one(
        {"_id": result.inserted_id}
    )


def get_ticket(ticket_id: str):
    return tickets_collection.find_one(
        {"ticket_id": ticket_id}
    )


def get_all_tickets():
    return list(
        tickets_collection.find()
    )


def search_tickets(query: dict):
    return list(
        tickets_collection.find(query)
    )


def update_ticket(
    ticket_id: str,
    update_data: dict,
):
    update_data["updated_at"] = datetime.now(
        timezone.utc
    )

    result = tickets_collection.update_one(
        {"ticket_id": ticket_id},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        return None

    return get_ticket(ticket_id)


def delete_ticket(ticket_id: str):
    result = tickets_collection.delete_one(
        {"ticket_id": ticket_id}
    )

    return result.deleted_count > 0
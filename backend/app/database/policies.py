from datetime import datetime, timezone

from backend.app.database.mongodb import database


policies_collection = database["policies"]



def create_policy(policy_data: dict):
    now = datetime.now(timezone.utc)

    policy = {
        **policy_data,
        "created_at": now,
        "updated_at": now,
    }

    result = policies_collection.insert_one(policy)

    return policies_collection.find_one(
        {"_id": result.inserted_id}
    )


def get_policy(policy_id: str):
    return policies_collection.find_one(
        {"policy_id": policy_id}
    )


def get_all_policies():
    return list(
        policies_collection.find()
    )


def search_policies(query: dict):
    return list(
        policies_collection.find(query)
    )


def update_policy(
    policy_id: str,
    update_data: dict,
):
    update_data["updated_at"] = datetime.now(
        timezone.utc
    )

    result = policies_collection.update_one(
        {"policy_id": policy_id},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        return None

    return get_policy(policy_id)


def delete_policy(policy_id: str):
    result = policies_collection.delete_one(
        {"policy_id": policy_id}
    )

    return result.deleted_count > 0
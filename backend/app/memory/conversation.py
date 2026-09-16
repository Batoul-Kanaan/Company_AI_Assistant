from datetime import datetime, timezone

from backend.app.database.mongodb import database


conversations_collection = database["conversations"]


def add_message(
    session_id: str,
    role: str,
    content: str,
    username: str = "system",
):
    message = {
        "username": username,
        "session_id": session_id,
        "role": role,
        "content": content,
        "created_at": datetime.now(timezone.utc),
    }

    conversations_collection.insert_one(message)


def get_messages(
    session_id: str,
    username: str = "system",
    limit: int = 20,
):
    return list(
        conversations_collection.find(
            {
                "username": username,
                "session_id": session_id,
            },
            {
                "_id": 0,
                "role": 1,
                "content": 1,
                "created_at": 1,
            },
        )
        .sort("created_at", 1)
        .limit(limit)
    )


def clear_session(session_id: str, username: str = "system"):
    result = conversations_collection.delete_many(
        {
            "username": username,
            "session_id": session_id,
        }
    )

    return result.deleted_count
import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017",
)
MONGO_DATABASE = os.getenv(
    "MONGO_DATABASE",
    "company_ai_assistant",
)

client = MongoClient(MONGO_URI)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

except ConnectionFailure:
    print("Failed to connect to MongoDB.")


database = client[MONGO_DATABASE]


documents_collection = database["documents"]

document_chunks_collection = database["document_chunks"]

employees_collection = database["employees"]

tickets_collection = database["tickets"]

conversations_collection = database["conversations"]


# Database indexes
employees_collection.create_index(
    "employee_id",
    unique=True,
)

employees_collection.create_index(
    "email",
    unique=True,
)

tickets_collection.create_index(
    "ticket_id",
    unique=True,
)


conversations_collection.create_index(
    [
        ("username", 1),
        ("session_id", 1),
        ("created_at", 1),
    ]
)
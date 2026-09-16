from backend.app.database.mongodb import documents_collection


print("Documents indexes:")
for index in documents_collection.list_indexes():
    print(index)

print("\nExisting documents:")

for document in documents_collection.find().limit(10):
    print(document)
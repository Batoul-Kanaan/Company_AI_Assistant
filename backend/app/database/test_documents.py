from backend.app.database.documents import (
    create_document,
    get_document,
    get_all_documents,
    search_documents,
    update_document,
    delete_document,
)


document_data = {
    "document_id": "DOC-TEST-001",
    "filename": "test_policy.pdf",
    "title": "Test Policy",
    "file_type": "pdf",
    "source": "internal",
    "uploaded_by": "EMP-001",
    "status": "processing",
}


print("=== CREATE ===")

document = create_document(document_data)

print(document)


print("\n=== GET ONE ===")

document = get_document("DOC-TEST-001")

print(document)


print("\n=== GET ALL ===")

documents = get_all_documents()

print(f"Total documents: {len(documents)}")


print("\n=== SEARCH ===")

documents = search_documents(
    {"status": "processing"}
)

print(f"Processing documents: {len(documents)}")


print("\n=== UPDATE ===")

updated_document = update_document(
    "DOC-TEST-001",
    {"status": "processed"},
)

print(updated_document)


print("\n=== DELETE ===")

deleted = delete_document(
    "DOC-TEST-001"
)

print("Deleted:", deleted)
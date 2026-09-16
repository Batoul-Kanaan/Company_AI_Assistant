from backend.app.ingestion.pipeline import ingest_pdf


PDF_PATH = "backend/uploads/random_test.pdf"


result = ingest_pdf(
    PDF_PATH,
    title="Random Test Document",
    uploaded_by="SYSTEM",
)


print("\n==============================")
print("INGESTION RESULT")
print("==============================")

print("Document ID:", result["document_id"])
print("Filename:", result["filename"])
print("Pages:", result["pages"])
print("Chunks:", result["chunks"])
print("Status:", result["status"])
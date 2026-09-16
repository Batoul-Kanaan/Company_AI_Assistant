from backend.app.ingestion.pdf_loader import load_pdf


PDF_PATH = "backend/uploads/random_test.pdf"


documents = load_pdf(PDF_PATH)

print(f"Number of pages: {len(documents)}")

for document in documents:
    print("\n--- PAGE ---")
    print(document.page_content)
    print("\nMetadata:")
    print(document.metadata)
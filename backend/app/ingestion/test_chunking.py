from backend.app.ingestion.pdf_loader import load_pdf
from backend.app.ingestion.text_splitter import split_documents


PDF_PATH = "backend/uploads/random_test.pdf"


documents = load_pdf(PDF_PATH)

chunks = split_documents(documents)

print(f"Number of pages: {len(documents)}")
print(f"Number of chunks: {len(chunks)}")

for index, chunk in enumerate(chunks):
    print("\n==============================")
    print(f"CHUNK {index + 1}")
    print("==============================")

    print(chunk.page_content)

    print("\nMetadata:")
    print(chunk.metadata)
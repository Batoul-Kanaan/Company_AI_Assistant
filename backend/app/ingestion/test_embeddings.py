from backend.app.ingestion.pdf_loader import load_pdf
from backend.app.ingestion.text_splitter import split_documents
from backend.app.ingestion.embeddings import get_embedding_model


PDF_PATH = "backend/uploads/random_test.pdf"


documents = load_pdf(PDF_PATH)

chunks = split_documents(documents)

embedding_model = get_embedding_model()

vector = embedding_model.embed_query(chunks[0].page_content)

print("Vector type:", type(vector))
print("Vector dimensions:", len(vector))

print("\nFirst 10 values:")
print(vector[:10])
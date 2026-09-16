from pathlib import Path
from uuid import uuid4
from backend.app.ingestion.pipeline import ingest_pdf
from backend.app.auth import verify_credentials

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from backend.app.database.documents import (
    create_document,
    delete_document,
    get_all_documents,
    get_document,
    search_documents,
    update_document,
)

from backend.app.models.document import (
    DocumentCreate,
    DocumentUpdate,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(verify_credentials)],   
)



def serialize_document(document: dict):
    if document:
        document["_id"] = str(document["_id"])

    return document



@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_document_route(
    document: DocumentCreate,
):
    existing_document = get_document(
        document.document_id
    )

    if existing_document:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Document already exists",
        )

    result = create_document(
        document.model_dump()
    )

    return serialize_document(result)



@router.get("/")
def get_documents():
    documents = get_all_documents()

    return [
        serialize_document(document)
        for document in documents
    ]



@router.get("/search")
def search_documents_route(
    status: str | None = None,
    source: str | None = None,
    file_type: str | None = None,
):
    query = {}

    if status:
        query["status"] = status

    if source:
        query["source"] = source

    if file_type:
        query["file_type"] = file_type

    documents = search_documents(query)

    return [
        serialize_document(document)
        for document in documents
    ]



@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    username: str = Depends(verify_credentials),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    upload_directory = Path("backend/uploads")

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_name = f"{uuid4()}_{file.filename}"
    file_path = upload_directory / file_name

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        ingestion_result = ingest_pdf(
            file_path=str(file_path),
            title=Path(file.filename).stem,
            uploaded_by=username,
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document ingestion failed. Please try again.",
        )
    finally:
        file_path.unlink(missing_ok=True)

    return {
        "message": "PDF uploaded and ingested successfully",
        "filename": file.filename,
        "ingestion": ingestion_result,
    }



@router.get("/{document_id}")
def get_document_route(
    document_id: str,
):
    document = get_document(
        document_id
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return serialize_document(document)



@router.put("/{document_id}")
def update_document_route(
    document_id: str,
    document: DocumentUpdate,
):
    existing_document = get_document(
        document_id
    )

    if not existing_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    updated_document = update_document(
        document_id,
        document.model_dump(
            exclude_unset=True
        ),
    )

    return serialize_document(
        updated_document
    )



@router.delete("/{document_id}")
def delete_document_route(
    document_id: str,
):
    deleted = delete_document(
        document_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return {
        "message": "Document deleted successfully"
    }
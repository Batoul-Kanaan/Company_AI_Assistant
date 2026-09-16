from datetime import datetime

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    document_id: str
    filename: str
    title: str
    file_type: str = "pdf"
    source: str = "internal"
    uploaded_by: str
    status: str = "processing"


class DocumentUpdate(BaseModel):
    filename: str | None = None
    title: str | None = None
    file_type: str | None = None
    source: str | None = None
    uploaded_by: str | None = None
    status: str | None = None


class DocumentInDB(DocumentCreate):
    created_at: datetime
    updated_at: datetime
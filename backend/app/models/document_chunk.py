from datetime import datetime, timezone

from pydantic import BaseModel, Field


class DocumentChunkCreate(BaseModel):
    document_id: str
    text: str
    source: str
    page: int
    chunk_index: int
    qdrant_point_id: str


class DocumentChunkInDB(DocumentChunkCreate):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
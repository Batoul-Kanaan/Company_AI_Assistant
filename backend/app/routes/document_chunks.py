from bson import ObjectId
from fastapi import APIRouter,Depends, HTTPException, status
from backend.app.auth import verify_credentials

from backend.app.database.document_chunks import (
    get_document_chunk,
    get_chunks_by_document,
    update_document_chunk,
    delete_document_chunk,
)

router = APIRouter(
    prefix="/document-chunks",
    tags=["Document Chunks"],
    dependencies=[Depends(verify_credentials)],
)


def serialize_chunk(chunk: dict):
    if chunk:
        chunk["_id"] = str(chunk["_id"])

    return chunk


def convert_to_object_id(chunk_id: str):
    if not ObjectId.is_valid(chunk_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document chunk ID",
        )

    return ObjectId(chunk_id)


@router.get("/document/{document_id}")
def get_document_chunks_by_document(
    document_id: str,
):
    chunks = get_chunks_by_document(document_id)

    return [
        serialize_chunk(chunk)
        for chunk in chunks
    ]


@router.get("/{chunk_id}")
def get_document_chunk_route(
    chunk_id: str,
):
    object_id = convert_to_object_id(chunk_id)

    chunk = get_document_chunk(object_id)

    if not chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document chunk not found",
        )

    return serialize_chunk(chunk)


@router.put("/{chunk_id}")
def update_document_chunk_route(
    chunk_id: str,
    update_data: dict,
):
    object_id = convert_to_object_id(chunk_id)

    chunk = get_document_chunk(object_id)

    if not chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document chunk not found",
        )

    updated_chunk = update_document_chunk(
        object_id,
        update_data,
    )

    return serialize_chunk(updated_chunk)


@router.delete("/{chunk_id}")
def delete_document_chunk_route(
    chunk_id: str,
):
    object_id = convert_to_object_id(chunk_id)

    deleted = delete_document_chunk(object_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document chunk not found",
        )

    return {
        "message": "Document chunk deleted successfully"
    }
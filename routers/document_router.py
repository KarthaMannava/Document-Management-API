from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile
)
from sqlalchemy.orm import Session
# from models.document import Document
from services.document_service import DocumentService
from schemas.document import Document, DocumentCreate, DocumentUpdate
from config.database import get_db

router = APIRouter()

@router.post("/upload")
def upload_document(file: UploadFile, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    return document_service.upload_document(file)


@router.get("/documents/{document_id}", response_model=Document)
def get_document(document_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a document by its ID.

    Args:
        document_id (int): The ID of the document.

    Returns:
        Document: The retrieved document.
    """
    document_service = DocumentService(db)
    document = document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/documents", response_model=List[Document])
def get_all_documents(db: Session = Depends(get_db)):
    """
    Retrieve all documents.

    Returns:
        List[Document]: A list of all documents.
    """
    document_service = DocumentService(db)
    return document_service.get_all_documents()


@router.post("/documents", response_model=Document)
def create_document(document_data: DocumentCreate, db: Session = Depends(get_db)):
    """
    Create a new document.

    Args:
        document_data (DocumentCreate): The data for creating the document.

    Returns:
        Document: The created document.
    """
    document_service = DocumentService(db)
    return document_service.create_document(document_data)


@router.put("/documents/{document_id}", response_model=Document)
def update_document(document_id: int, document_data: DocumentUpdate, db: Session = Depends(get_db)):
    """
    Update an existing document.

    Args:
        document_id (int): The ID of the document to update.
        document_data (DocumentUpdate): The updated data for the document.

    Returns:
        Document: The updated document.
    """
    document_service = DocumentService(db)
    document = document_service.update_document(document_id, document_data)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    """
    Delete a document.

    Args:
        document_id (int): The ID of the document to delete.

    Returns:
        dict: A dictionary indicating the success of the operation.
    """
    document_service = DocumentService(db)
    result = document_service.delete_document(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}


import time
import json
from uuid import uuid4
import magic
from typing import List, Optional, Union
from datetime import datetime
from fastapi import (
    status,
    HTTPException,
    UploadFile
)
from sqlalchemy.orm import Session
import boto3
from botocore.config import Config
from config.settings import get_settings
from repositories.document_repository import DocumentRepository
from schemas.document import Document, DocumentCreate, DocumentUpdate

TIME_STR = time.strftime("%Y-%m-%d-%H:%M:%S")
KB = 1024
MB = 1024*KB
settings = get_settings()

config = Config(
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key
)

s3 = boto3.client('s3', config=config)
bucket = s3.Bucket(settings.aws_bucket_name)

SUPPORTED_FILE_TYPES = {
    'application/pdf': 'pdf',
    'image/png': 'png',
    'image/jpeg': 'jpeg'
}

class DocumentService:
    """
    Service class for handling document-related operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the DocumentService.

        Args:
            db (Session): The SQLAlchemy database session.
        """
        self.db = db
        self.repository = DocumentRepository(db)

    def get_document(self, document_id: int) -> Optional[Document]:
        """
        Retrieve a document by its ID.

        Args:
            document_id (int): The ID of the document.

        Returns:
            Optional[Document]: The retrieved document, or None if not found.
        """
        return self.repository.get_document(document_id)

    def get_all_documents(self) -> List[Document]:
        """
        Retrieve all documents.

        Returns:
            List[Document]: A list of all documents.
        """
        return self.repository.get_all_documents()

    def create_document(self, document_data: DocumentCreate) -> Document:
        """
        Create a new document.

        Args:
            document_data (DocumentCreate): The data for creating the document.

        Returns:
            Document: The created document.
        """
        document = Document(
            title=document_data.title,
            file_type=document_data.file_type,
            file_url=document_data.file_url,
            description=document_data.description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return self.repository.create_document(document)

    def update_document(self, document_id: int, document_data: DocumentUpdate) -> Optional[Document]:
        """
        Update an existing document.

        Args:
            document_id (int): The ID of the document to update.
            document_data (DocumentUpdate): The updated data for the document.

        Returns:
            Optional[Document]: The updated document, or None if not found.
        """
        document = self.repository.get_document(document_id)
        if document:
            document.title = document_data.title or document.title
            document.file_type = document_data.file_type or document.file_type
            document.file_url = document_data.file_url or document.file_url
            document.description = document_data.description or document.description
            document.updated_at = datetime.utcnow()
            return self.repository.update_document(document)
        return None

    def delete_document(self, document_id: int) -> bool:
        """
        Delete a document.

        Args:
            document_id (int): The ID of the document to delete.

        Returns:
            bool: True if the document was deleted successfully, False otherwise.
        """
        document = self.repository.get_document(document_id)
        if document:
            return self.repository.delete_document(document)
        return False
    
    def s3_upload(self, contents:bytes, key: str):
        # logger.info("Uploading {key} to s3") 
        bucket.put_object(key=key, Body=contents)
        
        
    def validate_file(file):
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No file found!!'
            )

        contents = file.read()
        file_size = len(contents)
        if not 0 < file_size <= 1 * MB:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Supported file size is 0 - 1 MB'
            )

        return contents


    def validate_file_type(contents):
        file_type = magic.from_buffer(buffer=contents, mime=True)
        if file_type not in SUPPORTED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Unsupported file type: {file_type}. Supported file types are {SUPPORTED_FILE_TYPES}'
            )

        return file_type


    def upload_document(self, file: Union[UploadFile, None] = None) -> None:
        contents = self.validate_file(file)
        file_type = self.validate_file_type(contents)
        key = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'
        self.s3_upload(contents=contents, key=key)
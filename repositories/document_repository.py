from sqlalchemy.orm import Session
import schemas.document as document_schemas
import models.document as document_models

class DocumentRepository:
    """
    Repository class for handling database operations related to documents.
    """

    def __init__(self, db: Session):
        """
        Initialize the DocumentRepository.

        Args:
            db (Session): The SQLAlchemy database session.
        """
        self.db = db

    def create_document(self, document: document_schemas.DocumentCreate):
        """
        Create a new document.

        Args:
            document (Document): The document to be created.
        """
        try:
            self.db.add(document)
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            self.db.close()

    def get_document(self, document_id: int):
        """
        Get a document by ID.

        Args:
            document_id (int): The ID of the document.

        Returns:
            Document: The retrieved document.
        """
        return self.db.query(document_models.Document).filter(document_models.Document.id == document_id).first()

    def update_document(self, document_data: document_schemas.DocumentUpdate):
        """
        Update an existing document.

        Args:
            document (Document): The document to be updated.
        """
        doc = self.db.query(document_models.Document).filter(document_models.Document.id == document_data.id).first()
        doc.title = document_data.get('title')
        doc.file_type = document_data.get('file_type')
        doc.file_url = document_data.get('file_url')
        doc.description = document_data.get('description')
        self.db.commit()

    def delete_document(self, document_id: int):
        """
        Delete a document by ID.

        Args:
            document_id (int): The ID of the document to be deleted.
        """
        doc = self.db.query(document_models.Document).filter(document_models.Document.id == document_id).first()
        return doc.delete()


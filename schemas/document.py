"""
This file defines the models for the Document entity in the application.
These models are used for data validation and serialization/deserialization.
"""
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class FileType(str, Enum):
    """
    Enumeration representing different file types.

    This enum class defines the available file types as string values.
    It allows us to restrict the file_type attribute to one of these predefined values.
    """

    PDF = "pdf"
    EXCEL = "excel"
    DOC = "doc"
    CSV = "csv"
    #TODO: Add more file types as needed


class DocumentBase(BaseModel):
    """
    Base model for document attributes.

    This base model defines the common attributes for a document.
    It will be used as a base for creating and updating document models.
    """

    title: str
    file_type: FileType
    file_url: str
    description: str


class DocumentCreate(DocumentBase):
    """
    Model for creating a new document.

    This model extends the DocumentBase model and adds the user_id attribute.
    It represents the data required to create a new document.
    """
    pass


class DocumentUpdate(DocumentBase):
    """
    Model for updating an existing document.

    This model extends the DocumentBase model without adding any additional attributes.
    It represents the data required to update the details of an existing document.
    """
    pass


class Document(DocumentBase):
    """
    Model representing a document.

    This model extends the DocumentBase model and adds the document_id, user_id,
    created_at, and updated_at attributes.
    It represents a document entity in the application.
    """

    document_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Pydantic model configuration.

        The orm_mode attribute allows the model to be used with SQLAlchemy's ORM.
        It instructs Pydantic to serialize and deserialize the model from the ORM mode.
        """

        orm_mode = True

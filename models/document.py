"""
This file defines the Document model for the application.
It represents a document entity in the database.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Document(Base):
    """
    Document model representing a document in the application.

    This model defines the attributes and structure of the Document entity.
    It is used for database ORM operations and data serialization/deserialization.
    They only specify the shape of data that’s flowing in and out of our REST interface. 
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    file_type = Column(String)
    file_url = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="documents")

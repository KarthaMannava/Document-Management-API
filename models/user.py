"""
This file defines the User model for the application.
It represents the user entity in the database.
"""
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from config.database import Base


class User(Base):
    """
    User model representing a user in the application.

    This model defines the attributes and structure of the User entity.
    It is used for database ORM operations and data serialization/deserialization.
    They only specify the shape of data that’s flowing in and out of our REST interface. 
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")

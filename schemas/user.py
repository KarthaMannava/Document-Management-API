"""
This file defines the schemas for the User entities in the application.
These schemas are used for data validation and serialization/deserialization.

The User models represent user-related data, including registration and authentication.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr
from schemas.document import Document


class UserBase(BaseModel):
    """
    Base model for user attributes.

    This base model defines the common attributes for a user.
    It will be used as a base for creating and updating user models.
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    Model for creating a new user.

    This model extends the UserBase model and adds the password attribute.
    It represents the data required to create a new user.
    """
    password: str

class UserUpdate(UserBase):
    """
    Model for updating an existing user.

    This model extends the UserBase model without adding any additional attributes.
    It represents the data required to update the details of an existing user.
    """
    pass


class User(UserBase):
    """
    Model representing a user.

    This model extends the UserBase model and adds the user_id, created_at,
    and updated_at attributes.
    It represents a user entity in the application.
    """

    id: int
    documents: list[Document] = []
    created_at: datetime
    updated_at: datetime
    token: str

    class Config:
        """
        Pydantic model configuration.

        The orm_mode attribute allows the model to be used with SQLAlchemy's ORM.
        It instructs Pydantic to serialize and deserialize the model from the ORM mode.
        """

        orm_mode = True

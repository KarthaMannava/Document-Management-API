from typing import List, Optional
from datetime import datetime
from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from schemas.user import User, UserCreate, UserUpdate
from utils.auth.auth_handler import verify_password
from services.jwt_service  import JWTService


class UserService:
    """
    Service class for handling user-related operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the UserService.

        Args:
            db (Session): The SQLAlchemy database session.
        """
        self.db = db
        self.repository = UserRepository(db)

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[User]: The retrieved user, or None if not found.
        """
        return self.repository.get_user(user_id)

    def get_all_users(self) -> List[User]:
        """
        Retrieve all users.

        Returns:
            List[User]: A list of all users.
        """
        return self.repository.get_all_users()

    def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user_data (UserCreate): The data for creating the user.

        Returns:
            User: The created user.
        # Example data for creating the access token
        """
        # Generate access token
        expires_delta = timedelta(hours=2)  # Set the token expiration time as desired
        token = JWTService.create_access_token(data={"sub": user_data.email}, expires_delta=expires_delta)
        # Assign the token to the user
        new_user = self.repository.create_user(user_data)
        new_user.token = token
        return new_user

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Update an existing user.

        Args:
            user_id (int): The ID of the user to update.
            user_data (UserUpdate): The updated data for the user.

        Returns:
            Optional[User]: The updated user, or None if not found.
        """
        user = self.repository.get_user(user_id)
        if user:
            user.username = user_data.username or user.username
            user.email = user_data.email or user.email
            user.updated_at = datetime.utcnow()
            return self.repository.update_user(user)
        return None

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.
        """
        user = self.repository.get_user(user_id)
        if user:
            return self.repository.delete_user(user)
        return False
    
    def authenticate_user(self, email: str, password: str):
        user = self.repository.get_user_by_email(self.db, email)
        if not user:
            return False

        # verify password is just auitil so it cant be moved here 
        if not verify_password(password, user.hashed_password):
            return False
        return user

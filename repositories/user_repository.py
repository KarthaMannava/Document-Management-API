from datetime import datetime
from sqlalchemy.orm import Session
import models.user as user_models
import schemas.user as user_schemas
from utils.auth.auth_handler import get_password_hash


class UserRepository:
    """
    Repository class for handling database operations related to users.
    """

    def __init__(self, db: Session):
        """
        Initialize the UserRepository.

        Args:
            db (Session): The SQLAlchemy database session.
        """
        self.db = db

    def create_user(self, user: user_schemas.UserCreate):
        """
        Create a new user.

        Args:
            user (User): The user to be created.
        """
        hashed_password = get_password_hash(user.password)
        new_user = user_models.User(email=user.email, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        return new_user

    def get_user(self, user_id: int):
        """
        Get a user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The retrieved user.
        """
        return self.db.query(user_models.User).filter(user_models.User.id == user_id).first()
    
    def get_user_by_email(self, email: str):
        return self.db.query(user_models.User).filter(user_models.User.email == email).first()
    
    def get_users(self,skip: int = 0, limit: int = 100):
        return self.db.query(user_models.User).offset(skip).limit(limit).all()

    def update_user(self, user: user_schemas.User):
        """
        Update an existing user.

        Args:
            user (User): The user to be updated.
        """
        user = self.get_user(user.id)
        user.email = user.get('email')
        user.is_active = user.get('is_active')
        self.db.commit()
        return user

    def delete_user(self, user_id: int):
        """
        Delete a user by ID.

        Args:
            user_id (int): The ID of the user to be deleted.
        """
        user = self.db.query(user_models.User).filter(user_models.User.id == user_id).first()
        user.delete()

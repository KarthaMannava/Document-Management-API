from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from models.user import User
from services.user_service import UserService
from schemas.user import User,UserCreate, UserUpdate
import schemas.user as user_schemas
from config.database import get_db


router = APIRouter()


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The retrieved user.
    """
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all users.

    Returns:
        List[User]: A list of all users.
    """
    user_service = UserService(db)
    return user_service.get_all_users()


@router.post("/user/signup", response_model=user_schemas.User)
def user_signup(user_data: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user_data (UserCreate): The data for creating the user.

    Returns:
        User: The created user.
    """
    user_service = UserService(db)
    return user_service.create_user(user_data)


@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user.

    Args:
        user_id (int): The ID of the user to update.
        user_data (UserUpdate): The updated data for the user.

    Returns:
        User: The updated user.
    """
    user_service = UserService(db)
    user = user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        dict: A dictionary indicating the success of the operation.
    """
    user_service = UserService(db)
    result = user_service.delete_user(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

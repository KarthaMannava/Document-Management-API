"""
This module provides database connection and session management using SQLAlchemy.

It defines a function `get_db` that allows obtaining a database session for interacting with the database.

Author: Philip Mutua
Date: June 19, 2023
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.settings import get_settings

DATABASE_URL = get_settings().db_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Obtain a database session for interacting with the database.

    Returns:
        sqlalchemy.orm.Session: The database session.

    Yields:
        sqlalchemy.orm.Session: The database session.

    Examples:
        Usage of `get_db` function:
        ```
        with get_db() as db:
            # Use the database session `db` to interact with the database
            # ...
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

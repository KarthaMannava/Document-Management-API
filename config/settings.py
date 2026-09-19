"""
The `functools` module provides various utility functions, and `lru_cache` is one of them.
We are importing `lru_cache` from `functools` to enable caching for the `get_settings` function.
Caching improves performance by storing the results of expensive function calls and returning them directly from cache when the same inputs occur again.
"""

from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class represents the application's configuration settings.
    It inherits from `BaseSettings` provided by the `pydantic` library, allowing us to define and validate settings using type hints.
    """

    env_name: str = "Local"
    jwt_secret_key: str = "#%$&@^^@yyetet%$%#$"
    jwt_algorithm: str = ""
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./db.sqlite"
    aws_access_key_id: str = ''
    aws_secret_access_key: str = ''
    aws_bucket_name: str = ''
    aws_region: str = ''

    class Config:
        """
        Pydantic model configuration for the `Settings` class.

        The `env_file` attribute specifies the name of the environment file that should be loaded to override the default settings.
        It allows us to define environment-specific configurations without modifying the code.
        """

        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    Function to retrieve the application settings.

    This function uses the `lru_cache` decorator to enable caching for improved performance.
    It creates an instance of the `Settings` class and returns it.
    The decorator ensures that the function's results are cached and only calculated once, avoiding redundant processing.
    """

    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings

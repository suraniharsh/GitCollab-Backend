"""
Configuration Management Module
----------------------------

This module manages application-wide configuration settings using Pydantic's BaseSettings.
It handles environment variables, secrets, and application constants in a type-safe manner.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0

Features:
    - Environment variable loading with .env support
    - Type-safe configuration using Pydantic
    - Cached settings instance for performance
    - Secure handling of sensitive credentials
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings management using Pydantic BaseSettings.
    
    This class defines all configuration settings for the application,
    automatically loading values from environment variables or .env files.
    
    Attributes:
        API_V1_STR (str): API version prefix for all endpoints
        PROJECT_NAME (str): Name of the project
        GITHUB_TIMEOUT (int): Timeout for GitHub API requests in seconds
        GITHUB_MAX_RETRIES (int): Maximum number of retries for failed requests
        GITHUB_RETRY_DELAY (int): Delay between retries in seconds
        GITHUB_CLIENT_ID (str): OAuth client ID for GitHub authentication
        GITHUB_CLIENT_SECRET (str): OAuth client secret for GitHub authentication
        GITHUB_REDIRECT_URI (str): OAuth callback URL for GitHub authentication
        JWT_SECRET_KEY (str): Secret key for JWT token signing
        JWT_ALGORITHM (str): Algorithm used for JWT token signing
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES (int): JWT token expiration time
        LOG_LEVEL (str): Logging level for the application
        LOG_FORMAT (str): Format string for log messages
    """
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GitHub Inviter"
    
    # GitHub Settings
    GITHUB_TIMEOUT: int = 30
    GITHUB_MAX_RETRIES: int = 3
    GITHUB_RETRY_DELAY: int = 1
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    GITHUB_REDIRECT_URI: str = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/api/v1/auth/github/callback")
    
    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        """Pydantic configuration class."""
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env file

@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache a Settings instance.
    
    This function uses lru_cache to ensure that only one Settings instance
    is created during the application lifecycle, improving performance.
    
    Returns:
        Settings: Cached settings instance
    """
    return Settings()

settings = get_settings() 
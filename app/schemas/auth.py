"""
Authentication Schema Module
-------------------------

This module defines Pydantic models for authentication-related data structures,
including token responses and user authentication payloads.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0

Features:
    - JWT token response validation
    - User authentication data validation
    - Type-safe request/response models
"""

from pydantic import BaseModel
from typing import Dict, Any

class TokenResponse(BaseModel):
    """
    Schema for authentication token response.
    
    This model represents the response structure when a user successfully
    authenticates, containing their access token and user information.
    
    Attributes:
        access_token (str): JWT access token for authenticated requests
        token_type (str): Type of token (usually "bearer")
        user (Dict[str, Any]): User information from the authentication provider
        
    Example:
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "token_type": "bearer",
            "user": {
                "login": "username",
                "id": 12345,
                "name": "User Name"
            }
        }
    """
    access_token: str
    token_type: str
    user: Dict[str, Any] 
"""
Custom Exceptions Module
---------------------

This module defines custom exceptions for handling various error scenarios
in the application, particularly focusing on GitHub API interactions and
authentication failures.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0

Features:
    - GitHub API error handling
    - Authentication error handling
    - Rate limiting error handling
    - Resource not found error handling
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException, status 

class GitHubAPIError(Exception):
    """
    Custom exception for GitHub API errors.
    
    This exception is raised when the GitHub API returns an error response
    or when there are issues with the API communication.
    
    Attributes:
        message (str): Human-readable error message
        status_code (Optional[int]): HTTP status code from the API response
        response (Optional[Dict[str, Any]]): Raw API response data
        
    Example:
        ```python
        raise GitHubAPIError(
            message="Failed to invite user",
            status_code=422,
            response={"message": "User not found"}
        )
        ```
    """
    # Initialize GitHub API error with status code and response details
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code or 500
        self.response = response
        super().__init__(message)

class InvalidTokenError(HTTPException):
    """
    Exception for invalid or expired GitHub tokens.
    
    This exception is raised when the provided GitHub access token
    is invalid, expired, or has insufficient permissions.
    
    Attributes:
        status_code (int): HTTP 401 Unauthorized
        detail (str): Error message explaining the token issue
    """
    # Raise HTTP 401 for invalid or expired tokens
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired GitHub token"
        )

class RateLimitExceededError(HTTPException):
    """
    Exception for GitHub API rate limit exceeded.
    
    This exception is raised when the GitHub API rate limit is exceeded.
    It includes information about when the rate limit will reset.
    
    Attributes:
        status_code (int): HTTP 429 Too Many Requests
        detail (str): Error message with rate limit reset time
        
    Args:
        reset_time (str): Time when the rate limit will reset
    """
    # Raise HTTP 429 when rate limit is exceeded
    def __init__(self, reset_time: str):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"GitHub API rate limit exceeded. Reset at {reset_time}"
        )

class ResourceNotFoundError(HTTPException):
    """
    Exception for requested resource not found.
    
    This exception is raised when a requested GitHub resource
    (repository, organization, user, etc.) cannot be found.
    
    Attributes:
        status_code (int): HTTP 404 Not Found
        detail (str): Error message with resource details
        
    Args:
        resource_type (str): Type of resource (e.g., "Repository", "Organization")
        resource_name (str): Name of the resource that was not found
    """
    # Raise HTTP 404 when requested resource is not found
    def __init__(self, resource_type: str, resource_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_type} '{resource_name}' not found"
        ) 
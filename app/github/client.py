"""
GitHub API Client Module
----------------------

A robust and efficient client for interacting with the GitHub API.
Handles authentication, rate limiting, and provides a clean interface for repository
and organization management.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0

Features:
    - Async/await support for efficient API calls
    - Automatic rate limit handling
    - Proper error handling and logging
    - Context manager support for resource cleanup
"""

from typing import Optional, List, Dict, Any
import httpx
import asyncio
import logging
import os
from datetime import datetime
from ..core.exceptions import GitHubAPIError
from ..core.config import settings

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/github.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('github-client')

class GitHubClient:
    """
    Asynchronous GitHub API client with automatic rate limiting and error handling.
    
    This client provides methods for managing GitHub repository collaborators and
    organization members. It handles authentication, rate limiting, and provides
    detailed error information.
    
    Attributes:
        access_token (str): GitHub access token for authentication
        base_url (str): GitHub API base URL
        headers (Dict[str, str]): Common headers for API requests
        rate_limit (Dict[str, int]): Current rate limit status
        
    Usage:
        ```python
        async with GitHubClient(access_token) as github:
            await github.invite_to_repository(
                owner="owner",
                repo="repo",
                username="username",
                permission="write"
            )
        ```
    """
    
    # Initialize GitHub client with access token and configuration
    def __init__(self, access_token: str):
        """
        Initialize the GitHub client.
        
        Args:
            access_token (str): GitHub access token for authentication
        """
        self.access_token = access_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self._client: Optional[httpx.AsyncClient] = None
        self.rate_limit = {"remaining": 5000, "reset": 0}

    # Enter context manager and initialize HTTP client
    async def __aenter__(self):
        """Initialize the HTTP client when entering the context manager."""
        await self.init_client()
        return self

    # Exit context manager and cleanup resources
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the context manager."""
        await self.close()

    # Create async HTTP client with timeout and headers
    async def init_client(self):
        """Initialize the HTTP client if it hasn't been initialized."""
        if not self._client:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=settings.GITHUB_TIMEOUT
            )

    # Close HTTP client and free resources
    async def close(self):
        """Close the HTTP client and clean up resources."""
        if self._client:
            await self._client.aclose()
            self._client = None

    # Make HTTP request to GitHub API with rate limiting and error handling
    async def _make_request(
        self,
        method: str,
        url: str,
        json: Dict[str, Any] = None,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the GitHub API with rate limit handling.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, etc.)
            url (str): API endpoint URL
            json (Dict[str, Any], optional): JSON request body
            params (Dict[str, Any], optional): Query parameters
            
        Returns:
            Dict[str, Any]: JSON response from the API
            
        Raises:
            GitHubAPIError: If the API request fails
        """
        if not self._client:
            await self.init_client()

        try:
            response = await self._client.request(
                method=method,
                url=url,
                json=json,
                params=params
            )
            
            # Update rate limit info
            self.rate_limit = {
                "remaining": int(response.headers.get("X-RateLimit-Remaining", 5000)),
                "reset": int(response.headers.get("X-RateLimit-Reset", 0))
            }

            # Handle rate limiting
            if response.status_code == 403 and self.rate_limit["remaining"] == 0:
                reset_time = datetime.fromtimestamp(self.rate_limit["reset"])
                wait_time = (reset_time - datetime.now()).total_seconds()
                if wait_time > 0:
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds.")
                    await asyncio.sleep(wait_time)
                    return await self._make_request(method, url, json, params)

            # Log the response for debugging
            logger.info(f"GitHub API Response: {response.status_code} - {response.text}")

            # Check if user exists before proceeding
            if response.status_code == 404 and "Not Found" in response.text:
                raise GitHubAPIError(
                    message=f"User not found or doesn't exist",
                    status_code=404
                )

            response.raise_for_status()
            return response.json() if response.content else {}

        except httpx.HTTPStatusError as e:
            error_msg = f"GitHub API error: {e.response.text}"
            logger.error(error_msg)
            raise GitHubAPIError(
                message=error_msg,
                status_code=e.response.status_code,
                response=e.response.json() if e.response.content else None
            )
        except httpx.RequestError as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            raise GitHubAPIError(message=error_msg)

    # Invite user to repository with specified permissions
    async def invite_to_repository(
        self,
        owner: str,
        repo: str,
        username: str,
        permission: str = "write"
    ) -> Dict[str, Any]:
        """
        Invite a user to a repository with specified permissions.
        
        Args:
            owner (str): Repository owner username
            repo (str): Repository name
            username (str): Username to invite
            permission (str, optional): Permission level. Defaults to "write".
                Possible values: "read", "write", "admin"
                
        Returns:
            Dict[str, Any]: Response from the GitHub API
            
        Raises:
            GitHubAPIError: If the user doesn't exist or the invitation fails
        """
        # First check if user exists
        await self.get_user_info(username)
        
        url = f"/repos/{owner}/{repo}/collaborators/{username}"
        return await self._make_request(
            method="PUT",
            url=url,
            json={"permission": permission}
        )

    # Invite user to organization with specified role
    async def invite_to_organization(
        self,
        org: str,
        username: str,
        role: str = "member"
    ) -> Dict[str, Any]:
        """
        Invite a user to an organization with specified role.
        
        Args:
            org (str): Organization name
            username (str): Username to invite
            role (str, optional): Role in the organization. Defaults to "member".
                Possible values: "member", "admin"
                
        Returns:
            Dict[str, Any]: Response from the GitHub API
            
        Raises:
            GitHubAPIError: If the user doesn't exist or the invitation fails
        """
        # First check if user exists and get user info
        user_info = await self.get_user_info(username)
        
        # Check if user is already a member
        try:
            member_status = await self._make_request(
                method="GET",
                url=f"/orgs/{org}/memberships/{username}"
            )
            if member_status.get("state") in ["active", "pending"]:
                return {"state": member_status["state"], "message": f"User is already {member_status['state']} in the organization"}
        except GitHubAPIError as e:
            if e.status_code != 404:  # If error is not "Not Found", re-raise it
                raise

        # Send the invitation using the memberships endpoint
        url = f"/orgs/{org}/memberships/{username}"
        return await self._make_request(
            method="PUT",
            url=url,
            json={"role": role}
        )

    # Verify GitHub user exists and return user information
    async def get_user_info(self, username: str) -> Dict[str, Any]:
        """
        Get information about a GitHub user.
        
        Args:
            username (str): GitHub username to look up
            
        Returns:
            Dict[str, Any]: User information from the GitHub API
            
        Raises:
            GitHubAPIError: If the user doesn't exist
        """
        url = f"/users/{username}"
        return await self._make_request("GET", url) 
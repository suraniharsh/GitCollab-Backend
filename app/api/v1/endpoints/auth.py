"""
GitHub OAuth Authentication Endpoints
---------------------------------

This module provides FastAPI endpoints for handling GitHub OAuth authentication flow.
It manages the OAuth2 authorization code grant flow with GitHub's OAuth service.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0

Features:
    - GitHub OAuth2 authentication flow
    - Access token exchange
    - User information retrieval
    - Secure token handling
    - Error handling for OAuth failures

Flow:
    1. User is redirected to GitHub login (/login/github)
    2. After GitHub authorization, user is redirected back (/github/callback)
    3. Code is exchanged for access token
    4. User information is retrieved
    5. Token response is returned
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
from urllib.parse import urlencode
from ....core.config import settings
from ....schemas.auth import TokenResponse
from ....core.exceptions import GitHubAPIError

router = APIRouter()

@router.get(
    "/login/github",
    summary="Initiate GitHub OAuth Flow",
    description="Redirects the user to GitHub's authorization page to begin the OAuth flow",
    response_class=RedirectResponse,
    responses={
        302: {"description": "Redirect to GitHub authorization page"},
        400: {"description": "Invalid client configuration"}
    }
)
# Redirect user to GitHub OAuth authorization page
async def github_login():
    """
    Start the GitHub OAuth flow by redirecting to GitHub's authorization page.
    
    This endpoint constructs the GitHub OAuth authorization URL with the necessary
    parameters and redirects the user to begin the authentication process.
    
    The following OAuth scopes are requested:
    - repo: Full control of private repositories
    - admin:org: Full control of orgs and teams
    - read:org: Read org and team membership
    
    Returns:
        RedirectResponse: Redirect to GitHub's authorization page
        
    Raises:
        HTTPException: If client configuration is invalid
    """
    # Build the OAuth authorization parameters
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,  # Our application's GitHub OAuth client ID
        "redirect_uri": settings.GITHUB_REDIRECT_URI,  # Where GitHub will redirect back after auth
        "scope": "repo admin:org read:org"  # Permissions we're requesting from the user
    }
    # Construct the full GitHub authorization URL with encoded parameters
    github_auth_url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    # Redirect the user to GitHub's authorization page
    return RedirectResponse(url=github_auth_url)

@router.get(
    "/github/callback",
    summary="GitHub OAuth Callback",
    description="Handles the callback from GitHub OAuth and exchanges the code for an access token",
    response_model=TokenResponse,
    responses={
        200: {
            "description": "Successfully authenticated with GitHub",
            "model": TokenResponse
        },
        400: {"description": "Invalid authorization code or OAuth error"},
        500: {"description": "GitHub API communication error"}
    }
)
# Exchange OAuth code for access token and retrieve user info
async def github_callback(code: str):
    """
    Handle the GitHub OAuth callback and exchange code for access token.
    
    This endpoint is called by GitHub after successful user authorization.
    It exchanges the temporary code for an access token and retrieves the
    user's information from GitHub.
    
    Args:
        code (str): Temporary authorization code from GitHub
        
    Returns:
        TokenResponse: Access token and user information
        
    Raises:
        HTTPException: If the OAuth flow fails or the code is invalid
        GitHubAPIError: If there are issues communicating with GitHub's API
        
    Example Response:
        ```json
        {
            "access_token": "gho_16C7e42F292c6912E7710c838347Ae178B4a",
            "token_type": "bearer",
            "user": {
                "login": "username",
                "id": 12345,
                "name": "User Name",
                "email": "user@example.com"
            }
        }
        ```
    """
    try:
        # Create an async HTTP client for making requests to GitHub
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": settings.GITHUB_REDIRECT_URI
                }
            )
            # Parse the JSON response containing the access token
            token_data = token_response.json()
            
            # Check if GitHub returned an error (e.g., invalid code, expired code)
            if "error" in token_data:
                raise HTTPException(
                    status_code=400,  # Bad Request - the authorization failed
                    detail=f"GitHub OAuth error: {token_data['error_description']}"
                )
            
            # Extract the access token from the response
            access_token = token_data.get("access_token")
            
            user_response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json"
                }
            )
            # Parse the user information from the response
            user_data = user_response.json()
            
            # Return the access token and user information in a structured response
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user=user_data
            )
            
    except httpx.HTTPError as e:
        # Handle any HTTP errors that occurred during the OAuth process
        raise GitHubAPIError(
            message="Failed to authenticate with GitHub",
            status_code=e.response.status_code if hasattr(e, 'response') else 500
        ) 
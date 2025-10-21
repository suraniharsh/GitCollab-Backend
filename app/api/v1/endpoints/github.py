"""
GitHub Invitation Endpoints Module
-------------------------------

This module provides FastAPI endpoints for managing GitHub repository and organization invitations.
It handles authentication, rate limiting, and provides detailed responses for invitation operations.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0

Endpoints:
    - POST /invite/repository: Invite users to a GitHub repository
    - POST /invite/organization: Invite users to a GitHub organization

Authentication:
    Requires a GitHub access token in the Authorization header:
    Authorization: Bearer <github_token>
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import asyncio

from ....github.client import GitHubClient
from ....schemas.github import InvitationBase, BatchInvitationResponse, InvitationResponse
from ....core.exceptions import GitHubAPIError, InvalidTokenError, ResourceNotFoundError

router = APIRouter()
security = HTTPBearer()

@router.post(
    "/invite/repository",
    response_model=BatchInvitationResponse,
    summary="Invite multiple users to a repository",
    description="""
    Invite multiple users to a GitHub repository with specified permissions.
    
    The target repository must be specified in the format 'owner/repo'.
    Requires authentication with a GitHub token that has repository admin access.
    
    Permission levels:
    - read: Read-only access
    - write: Read and write access
    - admin: Full administrative access
    """,
    response_description="Results of the invitation operations with success/failure counts"
)
# Invite multiple users to a repository with error handling
async def invite_to_repository(
    request: InvitationBase,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Invite multiple users to a GitHub repository.
    
    Args:
        request (InvitationBase): The invitation request containing:
            - users: List of GitHub usernames to invite
            - target_name: Repository name in format 'owner/repo'
            - permission_level: Permission level (read, write, admin)
        credentials (HTTPAuthorizationCredentials): GitHub access token
    
    Returns:
        BatchInvitationResponse: Results of the invitation operations
        
    Raises:
        HTTPException: If the repository format is invalid
        GitHubAPIError: If there are issues with the GitHub API
    """
    try:
        owner, repo = request.target_name.split("/")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # HTTP 400
            detail="target_name must be in format 'owner/repo'"
        )

    access_token = credentials.credentials
    results: List[InvitationResponse] = []
    
    # Use context manager to ensure proper cleanup of HTTP client
    async with GitHubClient(access_token) as github:
        for username in request.users:
            try:
                response = await github.invite_to_repository(
                    owner=owner,
                    repo=repo,
                    username=username,
                    permission=request.permission_level
                )
                
                # Check if invitation was successful
                if response.get("state") == "pending":
                    results.append(InvitationResponse(
                        username=username,
                        status="success",
                        message="Invitation sent successfully"
                    ))
                else:
                    results.append(InvitationResponse(
                        username=username,
                        status="success",
                        message=response.get("message", "User has been added to the repository")
                    ))
                    
            except GitHubAPIError as e:
                # Handle errors for individual users
                error_message = str(e)
                if "already a collaborator" in error_message.lower():
                    results.append(InvitationResponse(
                        username=username,
                        status="info",
                        message="User is already a collaborator"
                    ))
                else:
                    # Other errors (user not found, permission denied, etc.)
                    results.append(InvitationResponse(
                        username=username,
                        status="error",
                        message=error_message
                    ))
            # Add a small delay between requests to avoid rate limiting
            await asyncio.sleep(0.5)

    return BatchInvitationResponse.from_results(results)

@router.post(
    "/invite/organization",
    response_model=BatchInvitationResponse,
    summary="Invite multiple users to an organization",
    description="""
    Invite multiple users to a GitHub organization with specified roles.
    
    Requires authentication with a GitHub token that has organization admin access.
    The organization must have third-party access enabled for the OAuth app.
    
    Permission levels:
    - member: Regular member access
    - admin: Organization administrator access
    """,
    response_description="Results of the invitation operations with success/failure counts"
)
# Invite multiple users to an organization with error handling
async def invite_to_organization(
    request: InvitationBase,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Invite multiple users to a GitHub organization.
    
    Args:
        request (InvitationBase): The invitation request containing:
            - users: List of GitHub usernames to invite
            - target_name: Organization name
            - permission_level: Permission level (member, admin)
        credentials (HTTPAuthorizationCredentials): GitHub access token
    
    Returns:
        BatchInvitationResponse: Results of the invitation operations
        
    Raises:
        GitHubAPIError: If there are issues with the GitHub API
    """
    # Extract the access token from the Authorization header
    access_token = credentials.credentials
    results: List[InvitationResponse] = []
    
    # Use context manager to ensure proper cleanup of HTTP client
    async with GitHubClient(access_token) as github:
        for username in request.users:
            try:
                response = await github.invite_to_organization(
                    org=request.target_name,
                    username=username,
                    role="member" if request.permission_level == "write" else request.permission_level
                )
                
                if response.get("state") == "active":
                    # User is already an active member
                    results.append(InvitationResponse(
                        username=username,
                        status="success",
                        message="User is already an active member"
                    ))
                elif response.get("state") == "pending":
                    # Invitation sent, waiting for user to accept
                    results.append(InvitationResponse(
                        username=username,
                        status="success",
                        message="Invitation sent successfully"
                    ))
                else:
                    # Other successful outcomes
                    results.append(InvitationResponse(
                        username=username,
                        status="success",
                        message=response.get("message", "User has been invited to the organization")
                    ))
                    
            except GitHubAPIError as e:
                results.append(InvitationResponse(
                    username=username,
                    status="error",
                    message=str(e)
                ))
            # Add a small delay between requests to avoid rate limiting
            await asyncio.sleep(0.5)

    return BatchInvitationResponse.from_results(results) 
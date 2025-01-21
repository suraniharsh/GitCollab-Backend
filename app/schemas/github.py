"""
GitHub Invitation Schemas Module
------------------------------

This module defines the Pydantic models for handling GitHub repository and organization invitations.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class InvitationBase(BaseModel):
    """
    Base model for GitHub invitation requests.
    
    Attributes:
        users (List[str]): List of GitHub usernames to invite
        target_name (str): Target repository (owner/repo) or organization name
        permission_level (str): Permission level for the invitation
            - For repositories: "read", "write", "admin"
            - For organizations: "member", "admin"
    """
    users: List[str] = Field(
        ...,
        description="List of GitHub usernames to invite",
        example=["username1", "username2"]
    )
    target_name: str = Field(
        ...,
        description="Repository name (owner/repo) or organization name",
        example="owner/repo-name or org-name"
    )
    permission_level: str = Field(
        default="write",
        description="Permission level for repository (read, write, admin) or organization (member, admin)",
        example="write"
    )

class InvitationResponse(BaseModel):
    """
    Response model for individual invitation results.
    
    Attributes:
        username (str): GitHub username that was invited
        status (str): Status of the invitation ("success", "error", "info")
        message (str): Detailed message about the invitation result
    """
    username: str = Field(..., description="GitHub username that was invited")
    status: str = Field(..., description="Status of the invitation (success/error/info)")
    message: str = Field(..., description="Detailed message about the invitation result")

class BatchInvitationResponse(BaseModel):
    """
    Response model for batch invitation operations.
    
    This model aggregates the results of multiple invitation attempts and provides
    summary statistics about successful and failed invitations.
    
    Attributes:
        results (List[InvitationResponse]): List of individual invitation results
        successful (int): Number of successful invitations (including existing members)
        failed (int): Number of failed invitations
    
    Example:
        {
            "results": [
                {
                    "username": "user1",
                    "status": "success",
                    "message": "Invitation sent successfully"
                }
            ],
            "successful": 1,
            "failed": 0
        }
    """
    results: List[InvitationResponse] = Field(
        ...,
        description="List of individual invitation results"
    )
    successful: int = Field(
        ...,
        description="Number of successful invitations"
    )
    failed: int = Field(
        ...,
        description="Number of failed invitations"
    )
    
    @classmethod
    def from_results(cls, results: List[InvitationResponse]) -> "BatchInvitationResponse":
        """
        Create a BatchInvitationResponse from a list of InvitationResponse objects.
        
        Args:
            results (List[InvitationResponse]): List of invitation results
            
        Returns:
            BatchInvitationResponse: Aggregated response with success/failure counts
        """
        # Count both success and info status as successful
        successful = sum(1 for r in results if r.status in ["success", "info"])
        return cls(
            results=results,
            successful=successful,
            failed=len(results) - successful
        ) 
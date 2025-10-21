"""
FastAPI Application Entry Point
----------------------------

This module serves as the main entry point for the FastAPI application.
It configures the application, sets up middleware, and includes routers
for different API endpoints.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0

Features:
    - FastAPI application configuration
    - CORS middleware setup
    - API versioning
    - Health check endpoints
    - Authentication and GitHub API routes
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.api.v1.endpoints import github as github_router
from app.api.v1.endpoints import auth as auth_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A simple API to invite multiple users to GitHub organizations and repositories",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth_router.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"]
)

app.include_router(
    github_router.router, 
    prefix=settings.API_V1_STR,
    tags=["github"]
)

# Root endpoint - provides basic information about the API
@app.get("/", tags=["health"])
async def root():
    """
    Root endpoint to check if the API is running and get basic information.
    
    This endpoint provides basic information about the API, including:
    - Current status
    - API version
    - Documentation URL
    - Available endpoints
    
    Returns:
        dict: API information and status
        
    Example:
        ```json
        {
            "status": "online",
            "version": "1.0.0",
            "docs_url": "/docs",
            "endpoints": {
                "auth": "/api/v1/auth/login/github",
                "repository_invite": "/api/v1/invite/repository",
                "organization_invite": "/api/v1/invite/organization"
            }
        }
        ```
    """
    return {
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs",
        "endpoints": {
            "auth": f"{settings.API_V1_STR}/auth/login/github",
            "repository_invite": f"{settings.API_V1_STR}/invite/repository",
            "organization_invite": f"{settings.API_V1_STR}/invite/organization"
        }
    }

# Health check endpoint for monitoring and load balancers
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    This endpoint can be used by monitoring tools and load balancers
    to check if the application is running and healthy.
    
    Returns:
        dict: Health status of the application
        
    Example:
        ```json
        {
            "status": "healthy"
        }
        ```
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    # Run the application using uvicorn server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )

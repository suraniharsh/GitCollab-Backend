# Installation Guide

This guide will help you set up the GitHub Collaboration Backend service on your system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Step-by-Step Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/suraniharsh/gitcollab-backend.git
   cd gitcollab-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_ORG=your_github_organization
   LOG_LEVEL=INFO
   ```

## Configuration

See the [Configuration](configuration.md) guide for detailed information about available settings and environment variables.

## Running the Application

1. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Verifying Installation

1. Check the health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

2. The response should be:
   ```json
   {
     "status": "healthy",
     "timestamp": "..."
   }
   ```

## Troubleshooting

If you encounter any issues during installation:

1. Ensure all prerequisites are properly installed
2. Check the logs in the `logs/` directory
3. Verify your environment variables are correctly set
4. Make sure your GitHub token has the required permissions 
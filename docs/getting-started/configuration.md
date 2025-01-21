# Configuration Guide

This guide covers all configuration options available in the GitHub Collaboration Backend service. The application uses environment variables for configuration, which can be set either directly in your environment or through a `.env` file.

## Environment Variables

### Required Variables

These environment variables must be set for the application to function properly:

```env
GITHUB_CLIENT_ID=your_github_oauth_app_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_app_client_secret
JWT_SECRET_KEY=your_secure_jwt_secret
```

### Optional Variables

These variables have default values but can be customized:

```env
# GitHub Settings
GITHUB_REDIRECT_URI=http://localhost:8000/api/v1/auth/github/callback
GITHUB_TIMEOUT=30
GITHUB_MAX_RETRIES=3
GITHUB_RETRY_DELAY=1

# JWT Settings
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Configuration Details

### API Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `API_V1_STR` | API version prefix for all endpoints | `/api/v1` |
| `PROJECT_NAME` | Name of the project | `GitHub Inviter` |

### GitHub Settings

| Setting | Description | Default | Required |
|---------|-------------|---------|----------|
| `GITHUB_CLIENT_ID` | OAuth client ID from GitHub | - | Yes |
| `GITHUB_CLIENT_SECRET` | OAuth client secret from GitHub | - | Yes |
| `GITHUB_REDIRECT_URI` | OAuth callback URL | `http://localhost:8000/api/v1/auth/github/callback` | No |
| `GITHUB_TIMEOUT` | API request timeout in seconds | 30 | No |
| `GITHUB_MAX_RETRIES` | Maximum retries for failed requests | 3 | No |
| `GITHUB_RETRY_DELAY` | Delay between retries in seconds | 1 | No |

### JWT Settings

| Setting | Description | Default | Required |
|---------|-------------|---------|----------|
| `JWT_SECRET_KEY` | Secret key for JWT signing | - | Yes |
| `JWT_ALGORITHM` | Algorithm for JWT signing | `HS256` | No |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 | No |

### Logging Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `LOG_LEVEL` | Application logging level | `INFO` |
| `LOG_FORMAT` | Log message format string | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` |

## Setting Up GitHub OAuth

1. Go to GitHub Developer Settings
2. Create a new OAuth App
3. Set the following:
   - Application name: Your app name
   - Homepage URL: Your frontend URL
   - Authorization callback URL: Your `GITHUB_REDIRECT_URI`
4. Copy the Client ID and generate a Client Secret
5. Add them to your `.env` file

## Example .env File

```env
# GitHub OAuth Settings
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:8000/api/v1/auth/github/callback

# Security
JWT_SECRET_KEY=your_secure_secret_key_here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Logging
LOG_LEVEL=DEBUG
```

## Configuration Best Practices

1. Never commit the `.env` file to version control
2. Use strong, unique values for secret keys
3. In production:
   - Use proper secret management
   - Set appropriate timeouts and retry values
   - Configure secure redirect URIs
   - Use appropriate logging levels 
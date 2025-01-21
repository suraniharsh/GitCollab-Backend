# Authentication API

The authentication system uses GitHub OAuth2 for secure user authentication. This documentation covers the available authentication endpoints and their usage.

## OAuth2 Flow

The authentication flow follows the standard OAuth2 authorization code grant flow:

1. User initiates login through the `/login/github` endpoint
2. User is redirected to GitHub for authorization
3. GitHub redirects back to `/github/callback` with an authorization code
4. Backend exchanges code for access token
5. Access token and user information are returned

## Endpoints

### Initiate GitHub Login

```http
GET /login/github
```

Redirects the user to GitHub's authorization page to begin the OAuth flow.

#### Response

- **Status Code**: 302 (Redirect)
- **Redirects to**: GitHub's authorization page

#### Error Responses

- **400 Bad Request**: Invalid client configuration

### GitHub OAuth Callback

```http
GET /github/callback
```

Handles the callback from GitHub OAuth and exchanges the authorization code for an access token.

#### Query Parameters

- `code` (string, required): The authorization code from GitHub

#### Response

```json
{
    "access_token": "string",
    "token_type": "bearer",
    "expires_in": 3600,
    "scope": "string",
    "user": {
        "login": "string",
        "name": "string",
        "email": "string"
    }
}
```

#### Error Responses

- **400 Bad Request**: Invalid authorization code or OAuth error
- **500 Internal Server Error**: GitHub API communication error

## Security Considerations

1. All tokens are transmitted over HTTPS
2. Access tokens are never logged or stored
3. Token expiration is handled automatically
4. Scope restrictions are enforced

## Example Usage

### Using cURL

```bash
# Step 1: Open this URL in a browser
curl -L http://localhost:8000/login/github

# Step 2: After GitHub redirect, you'll get a response with the token
# The callback is handled automatically by the browser
```

### Using JavaScript

```javascript
// Redirect user to GitHub login
window.location.href = 'http://localhost:8000/login/github';

// Handle the callback in your frontend route
// The backend will process the code and return the token
``` 
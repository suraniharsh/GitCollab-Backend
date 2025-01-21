# Deployment Guide

This guide covers how to deploy the GitHub Collaboration Backend to various platforms, with a focus on Vercel deployment.

## Deploying to Vercel

### Prerequisites

1. [Vercel Account](https://vercel.com/signup)
2. [Vercel CLI](https://vercel.com/cli) (optional for local testing)
3. GitHub account with your repository

### Step-by-Step Deployment

1. **Prepare Your Repository**
   - Ensure your repository has the following files:
     - `vercel.json`
     - `requirements.txt`
     - `main.py`
     - `.env` (you'll add these values in Vercel's dashboard)

2. **Deploy Using Vercel Dashboard**
   
   a. Go to [Vercel Dashboard](https://vercel.com/dashboard)
   
   b. Click "New Project"
   
   c. Import your GitHub repository
   
   d. Configure project:
      - Framework Preset: Other
      - Build and Output Settings: Leave as default
      - Environment Variables: Add the following
        ```
        GITHUB_CLIENT_ID=your_github_oauth_app_client_id
        GITHUB_CLIENT_SECRET=your_github_oauth_app_client_secret
        JWT_SECRET_KEY=your_secure_jwt_secret
        GITHUB_REDIRECT_URI=https://your-vercel-domain.vercel.app/api/v1/auth/github/callback
        ```
   
   e. Click "Deploy"

3. **Update GitHub OAuth App**
   
   After deployment, update your GitHub OAuth App settings:
   - Homepage URL: `https://your-vercel-domain.vercel.app`
   - Authorization callback URL: `https://your-vercel-domain.vercel.app/api/v1/auth/github/callback`

### Using Vercel CLI (Optional)

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from your project directory:
   ```bash
   vercel
   ```

4. For production deployment:
   ```bash
   vercel --prod
   ```

### Environment Variables

Make sure to set these environment variables in Vercel's dashboard:

| Variable | Description |
|----------|-------------|
| `GITHUB_CLIENT_ID` | Your GitHub OAuth App client ID |
| `GITHUB_CLIENT_SECRET` | Your GitHub OAuth App client secret |
| `JWT_SECRET_KEY` | Secret key for JWT token signing |
| `GITHUB_REDIRECT_URI` | OAuth callback URL (Vercel domain) |
| `LOG_LEVEL` | Optional: Logging level (default: INFO) |

### Deployment Configuration

The `vercel.json` file configures how your application is built and served:

```json
{
    "version": 2,
    "builds": [
        {
            "src": "main.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "main.py"
        }
    ],
    "env": {
        "PYTHONPATH": ".",
        "MAX_WORKERS": "1"
    }
}
```

### Vercel Specific Considerations

1. **Cold Starts**: Serverless functions may experience cold starts
2. **Timeout Limits**: Functions timeout after 10s (Hobby) or 60s (Pro)
3. **Environment Size**: Code + dependencies must be under 50MB
4. **Stateless**: Don't rely on local file system storage

### Troubleshooting

1. **Deployment Fails**:
   - Check build logs in Vercel dashboard
   - Verify requirements.txt is correct
   - Ensure all dependencies are compatible

2. **Runtime Errors**:
   - Check Function Logs in Vercel dashboard
   - Verify environment variables are set
   - Check GitHub OAuth settings

3. **OAuth Issues**:
   - Verify redirect URIs match exactly
   - Check GitHub App settings
   - Ensure environment variables are correct

### Monitoring and Logs

1. Access logs through Vercel dashboard:
   - Deployment logs
   - Function logs
   - Runtime errors

2. Set up monitoring:
   - Enable Vercel Analytics
   - Configure error reporting
   - Set up status notifications

### Best Practices

1. **Security**:
   - Use environment variables for secrets
   - Enable HTTPS-only access
   - Regularly rotate JWT secrets

2. **Performance**:
   - Optimize cold starts
   - Use appropriate cache headers
   - Keep dependencies minimal

3. **Maintenance**:
   - Regular dependency updates
   - Monitor error rates
   - Keep documentation updated 
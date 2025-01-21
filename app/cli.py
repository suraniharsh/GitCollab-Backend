"""
Command Line Interface Module
--------------------------

This module provides a command-line interface for the GitHub Inviter application.
It allows users to perform common operations without using the REST API directly.

Author: Harsh Surani (@suraniharsh)
License: MIT
Version: 1.0.0

Features:
    - GitHub repository invitation management
    - Organization member management
    - Batch operations support
    - Configuration management
    - Token management

Usage:
    python -m app.cli [command] [options]
    
Commands:
    invite-repo     Invite users to a repository
    invite-org      Invite users to an organization
    config          Manage application configuration
    token           Manage GitHub access tokens
"""

import click
import asyncio
import json
from typing import List
from .core.config import settings
from .github.client import GitHubClient

@click.group()
def cli():
    """
    GitHub Inviter CLI - Manage GitHub repository and organization invitations.
    
    This tool provides command-line access to GitHub Inviter functionality,
    allowing you to invite users to repositories and organizations efficiently.
    """
    pass

@cli.command()
@click.argument('repo', type=str)
@click.argument('users', nargs=-1)
@click.option(
    '--permission',
    type=click.Choice(['read', 'write', 'admin']),
    default='write',
    help='Permission level for invited users'
)
@click.option(
    '--token',
    envvar='GITHUB_TOKEN',
    help='GitHub access token (can also be set via GITHUB_TOKEN env var)'
)
async def invite_repo(repo: str, users: List[str], permission: str, token: str):
    """
    Invite users to a GitHub repository.
    
    Args:
        repo: Repository name in format 'owner/repo'
        users: List of GitHub usernames to invite
        permission: Permission level (read/write/admin)
        token: GitHub access token
        
    Example:
        python -m app.cli invite-repo owner/repo user1 user2 --permission write
    """
    try:
        async with GitHubClient(token) as client:
            owner, repo_name = repo.split('/')
            for user in users:
                try:
                    await client.invite_to_repository(
                        owner=owner,
                        repo=repo_name,
                        username=user,
                        permission=permission
                    )
                    click.echo(f"✓ Invited {user} to {repo} with {permission} access")
                except Exception as e:
                    click.echo(f"✗ Failed to invite {user}: {str(e)}", err=True)
    except ValueError:
        click.echo("Error: Repository must be in format 'owner/repo'", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('org')
@click.argument('users', nargs=-1)
@click.option(
    '--role',
    type=click.Choice(['member', 'admin']),
    default='member',
    help='Role in the organization'
)
@click.option(
    '--token',
    envvar='GITHUB_TOKEN',
    help='GitHub access token (can also be set via GITHUB_TOKEN env var)'
)
async def invite_org(org: str, users: List[str], role: str, token: str):
    """
    Invite users to a GitHub organization.
    
    Args:
        org: Organization name
        users: List of GitHub usernames to invite
        role: Organization role (member/admin)
        token: GitHub access token
        
    Example:
        python -m app.cli invite-org my-org user1 user2 --role member
    """
    try:
        async with GitHubClient(token) as client:
            for user in users:
                try:
                    await client.invite_to_organization(
                        org=org,
                        username=user,
                        role=role
                    )
                    click.echo(f"✓ Invited {user} to {org} as {role}")
                except Exception as e:
                    click.echo(f"✗ Failed to invite {user}: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--show', is_flag=True, help='Show current configuration')
@click.option('--set', 'set_value', type=(str, str), multiple=True, help='Set config value')
def config(show: bool, set_value: List[tuple]):
    """
    Manage application configuration.
    
    View or modify the application configuration settings.
    Sensitive values like tokens and secrets are masked.
    
    Args:
        show: Display current configuration
        set_value: Set configuration values (key-value pairs)
        
    Example:
        python -m app.cli config --show
        python -m app.cli config --set GITHUB_TIMEOUT 30
    """
    if show:
        config_dict = settings.dict()
        # Mask sensitive values
        for key in config_dict:
            if any(sensitive in key.lower() for sensitive in ['token', 'secret', 'key']):
                config_dict[key] = '********'
        click.echo(json.dumps(config_dict, indent=2))
    
    for key, value in set_value:
        # Implementation for setting config values would go here
        click.echo(f"Setting {key}={value}")

def main():
    """Entry point for the CLI application."""
    cli(_anyio_backend="asyncio")

if __name__ == "__main__":
    main() 
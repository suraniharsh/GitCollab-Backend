# Contributing Guide

Thank you for considering contributing to the GitHub Collaboration Backend! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gitcollab-backend.git
   cd gitcollab-backend
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `.\venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```
4. Set up your `.env` file following the [configuration guide](../getting-started/configuration.md)

## Code Style

We follow PEP 8 guidelines with some modifications:

- Line length: 100 characters
- Use type hints for function parameters and return values
- Use docstrings for modules, classes, and functions
- Sort imports using `isort`
- Format code using `black`

Example:
```python
from typing import Optional

def process_user(username: str, email: Optional[str] = None) -> dict:
    """
    Process user information.

    Args:
        username: The GitHub username
        email: Optional email address

    Returns:
        dict: Processed user information
    """
    return {
        "username": username,
        "email": email or f"{username}@github.com"
    }
```

## Git Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request

### Commit Message Format

We follow the Conventional Commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## Testing

1. Write tests for new features
2. Ensure all tests pass before submitting PR:
   ```bash
   pytest
   ```
3. Maintain or improve code coverage

## Documentation

1. Update documentation for new features
2. Include docstrings for new functions/classes
3. Update API documentation if endpoints change
4. Add examples for new functionality

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation
3. Add tests for new functionality
4. Ensure CI passes
5. Get review from maintainers

## Code Review

- Be respectful and constructive
- Focus on code, not the author
- Explain your reasoning
- Suggest improvements

## Getting Help

- Open an issue for bugs
- Use discussions for questions
- Join our community chat

## Security Issues

- Report security vulnerabilities privately
- Email: security@example.com
- Do not create public issues for security problems

## License

By contributing, you agree that your contributions will be licensed under the MIT License. 
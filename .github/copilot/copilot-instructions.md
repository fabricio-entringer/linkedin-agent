# GitHub Copilot Instructions

This file contains instructions for GitHub Copilot to follow when assisting with this repository.

## GitHub MCP Server Integration

- Use the GitHub Model Context Protocol (MCP) Server to manage topics from GitHub such as issues, PRs, and other GitHub-related tasks.
- Always integrate with the repository's GitHub MCP Server for context-aware assistance.

## Issue Creation Guidelines

When creating issues, follow these conventions based on the repository's branch naming standards:

### Issue Types

Issues should be categorized according to one of these types:
- `feature`: For new features or enhancements
- `bugfix`: For fixing non-critical bugs
- `hotfix`: For urgent production fixes
- `release`: For preparing a release branch
- `chore`: For maintenance tasks (e.g., updating dependencies, configs)
- `refactor`: For code improvements without changing behavior
- `docs`: For documentation updates only

### Issue Naming Convention

- Use clear, descriptive titles that reflect the content
- Keep titles concise but informative
- Use lowercase for consistency

## Working on Issues

### Branch Creation Requirement

- **ALWAYS** create a corresponding branch before starting work on a GitHub issue
- The branch must follow the naming convention below
- Format: `<type>/<description>` where the type should match the issue type
- Example: For issue #42 about adding a login feature, create branch `feature/add-login`

## Pull Request Guidelines

### PR Naming Convention

All PR titles must follow this format:
- Start with the issue number followed by the title
- Format: `#<issue-number> - <descriptive title>`
- Example: `#10 - Fix user authentication error`

### Branch Naming Convention

Branches should follow the pattern: `<type>/<description>`

Where:
- `<type>` is one of: feature, bugfix, hotfix, release, chore, refactor, docs
- `<description>` contains lowercase letters, numbers, dashes (-), underscores (_), or dots (.)

Examples of valid branch names:
- `feature/add-login-api`
- `bugfix/fix-user-profile`
- `hotfix/security-patch`
- `release/v1.2.0`
- `chore/update-dependencies`
- `refactor/clean-auth-service`
- `docs/update-readme`

Special branches 'master', and 'develop' are exempt from this naming pattern.

## General Guidance

- When suggesting changes, ensure they align with the repository's coding standards
- Always link PRs to related issues
- Follow the established project architecture and patterns
- When analyzing code, consider the project structure and existing patterns

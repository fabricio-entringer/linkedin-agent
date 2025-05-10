# Development Guide

This guide provides information for developers who want to contribute to or extend LinkedIn Agent.

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Chrome browser
- Git

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/fabricio-entringer/linkedin-agent.git
   cd linkedin-agent
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov pylint black  # Development tools
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your LinkedIn credentials and OpenAI API key
   ```

## Code Structure

```
├── app/                     # Main application directory
│   ├── agents/              # CrewAI agents
│   │   ├── agents.py        # Agent definitions
│   │   ├── tasks.py         # Task definitions
│   │   └── config/          # YAML configs
│   │       ├── agents.yaml  # Agent configurations
│   │       └── tasks.yaml   # Task configurations
│   ├── tools/               # Core functionality
│   │   ├── linkedin.py      # LinkedIn browser automation
│   │   └── linkedin_tools.py# Message analysis tools
│   └── utils/               # Utilities
│       ├── config.py        # Configuration functions
│       └── logger.py        # Logging setup
├── docs/                    # Documentation
├── logs/                    # Log files (generated at runtime)
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (from .env.example)
```

## Contribution Workflow

### Branching Model

Follow this branching strategy:

1. **Main Branches**:
   - `master` - Production-ready code
   - `develop` - Integration branch for features

2. **Feature Branches**:
   - Create from: `develop`
   - Merge back into: `develop`
   - Naming: `feature/description`

3. **Bugfix Branches**:
   - Create from: `develop`
   - Merge back into: `develop`
   - Naming: `bugfix/description`

4. **Hotfix Branches**:
   - Create from: `master`
   - Merge back into: `master` and `develop`
   - Naming: `hotfix/description`

5. **Release Branches**:
   - Create from: `develop`
   - Merge back into: `master` and `develop`
   - Naming: `release/version`

### Pull Request Process

1. Create a branch with the appropriate prefix (`feature/`, `bugfix/`, etc.)
2. Make your changes, following the coding standards
3. Write/update tests as needed
4. Ensure all tests pass
5. Submit a pull request to the appropriate target branch
6. Include a clear description of the changes and reference any related issues

### Coding Standards

Follow these standards for consistency:

1. **Code Formatting**:
   - Use [Black](https://black.readthedocs.io/) for Python formatting
   - Run `black .` before committing
   
2. **Linting**:
   - Use [Pylint](https://www.pylint.org/) to check your code
   - Run `pylint app` before committing
   
3. **Docstrings**:
   - Use [Google-style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
   - Document all classes and public methods

4. **Imports**:
   - Group imports in this order: standard library, third-party, local
   - Alphabetize imports within each group

5. **Error Handling**:
   - Use specific exceptions
   - Handle exceptions at appropriate levels
   - Log exceptions with meaningful messages

## Extending LinkedIn Agent

### Adding a New Feature

1. **Create a Feature Branch**:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/my-new-feature
   ```

2. **Implement Your Feature**:
   - Add new modules in the appropriate directories
   - Update existing code as needed
   - Add tests for your feature

3. **Test Your Feature**:
   ```bash
   # Run tests
   pytest -v
   
   # Check coverage
   pytest --cov=app
   
   # Run linting
   pylint app
   ```

4. **Submit a Pull Request**:
   - Push your branch
   - Create a pull request against the `develop` branch

### Modifying Browser Automation

To update or extend the LinkedIn browser automation:

1. Locate `app/tools/linkedin.py`
2. Identify the methods you need to modify
3. For new functionality, consider adding new methods rather than modifying existing ones
4. Always test changes thoroughly with both headless and visible browser modes

Example of adding a new method:

```python
def send_message(self, contact_name, message):
    """
    Send a message to a specific contact.
    
    Args:
        contact_name (str): Name of the contact to message
        message (str): Message content to send
        
    Returns:
        bool: Success status
    """
    try:
        # Implementation...
        return True
    except Exception as e:
        self.logger.error(f"Failed to send message: {str(e)}")
        return False
```

### Enhancing AI Response Generation

To improve or customize the AI response generation:

1. Examine the agent configurations in `app/agents/config/agents.yaml`
2. Modify the agent roles, goals, or backstories to change behavior
3. Update the task descriptions in `app/agents/config/tasks.yaml`
4. For more complex changes, update the agent initialization in `app/agents/agents.py`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_linkedin.py
```

### Writing Tests

When adding new features, include tests in the `tests/` directory:

```python
# Example test for a LinkedIn feature
def test_linkedin_login():
    # Mock setup
    mock_driver = MagicMock()
    tool = LinkedInTool()
    tool.driver = mock_driver
    
    # Test login success case
    mock_driver.find_element.return_value = MagicMock()
    result = tool.login()
    
    assert result is True
    # Additional assertions...
```

## Deployment

LinkedIn Agent is designed to run as a local tool, but can be deployed:

### Local Scheduled Running

Use cron (Linux/Mac) or Task Scheduler (Windows) to run the script periodically:

```bash
# Example cron job (runs every day at 9 AM)
0 9 * * * cd /path/to/linkedin-agent && ./venv/bin/python main.py
```

### Docker Deployment

A sample Dockerfile is provided for containerized deployment:

```dockerfile
FROM python:3.9-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run with headless mode
ENV HEADLESS=true

CMD ["python", "main.py"]
```

Build and run:

```bash
docker build -t linkedin-agent .
docker run --env-file .env linkedin-agent
```

## Troubleshooting Development Issues

See the [Troubleshooting](./troubleshooting.md) guide for common issues.

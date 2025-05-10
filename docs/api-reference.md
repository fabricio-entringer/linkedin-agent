# API Reference

This document provides detailed information about the classes, methods, and functions available in LinkedIn Agent.

## Main Classes

### LinkedInTool

The primary class for interacting with LinkedIn through browser automation.

**Location**: `app/tools/linkedin.py`

#### Methods:

| Method | Description | Parameters | Return Value |
|--------|-------------|------------|--------------|
| `__init__()` | Constructor | `headless`: bool | None |
| `start()` | Initializes the browser | None | Bool: Success status |
| `close()` | Closes the browser | None | None |
| `login()` | Logs into LinkedIn | None | Bool: Success status |
| `go_to_messages()` | Navigates to messages | None | Bool: Success status |
| `extract_messages()` | Extracts conversations | `limit`: int | Dict: Message data |
| `__wait_for_element()` | Waits for element | `by`, `selector` | WebElement |
| `__is_element_visible()` | Checks visibility | `by`, `selector` | Bool |

#### Usage Example:

```python
from app.tools.linkedin import LinkedInTool

# Initialize and start
tool = LinkedInTool(headless=False)
tool.start()

# Login and navigate
if tool.login():
    if tool.go_to_messages():
        # Extract messages
        messages = tool.extract_messages(limit=5)
        print(f"Extracted {len(messages)} conversations")

# Always close when done
tool.close()
```

### LinkedIn Analysis Tools

Functions for analyzing LinkedIn messages and generating responses.

**Location**: `app/tools/linkedin_tools.py`

#### Methods:

| Function | Description | Parameters | Return Value |
|----------|-------------|------------|--------------|
| `analyze_linkedin_messages()` | Analyzes messages with AI | `messages`: dict | str: Analysis results |

#### Usage Example:

```python
from app.tools.linkedin import LinkedInTool
from app.tools.linkedin_tools import analyze_linkedin_messages

# Extract messages
linkedin_tool = LinkedInTool()
linkedin_tool.start()
if linkedin_tool.login():
    if linkedin_tool.go_to_messages():
        messages = linkedin_tool.extract_messages()
        
        # Analyze messages
        if messages:
            results = analyze_linkedin_messages(messages)
            print(results)
            
linkedin_tool.close()
```

## CrewAI Components

### Agents

AI agents used for message analysis.

**Location**: `app/agents/agents.py`

#### Methods:

| Method | Description | Parameters | Return Value |
|--------|-------------|------------|--------------|
| `initialize_agents()` | Creates agent instances | `config`: dict | List: Agent objects |

### Tasks

Tasks assigned to agents.

**Location**: `app/agents/tasks.py`

#### Methods:

| Method | Description | Parameters | Return Value |
|--------|-------------|------------|--------------|
| `initialize_tasks()` | Creates task instances | `config`: dict | List: Task objects |

## Utility Functions

### Logger

Logging utilities.

**Location**: `app/utils/logger.py`

#### Functions:

| Function | Description | Parameters | Return Value |
|----------|-------------|------------|--------------|
| `setup_logger()` | Configures logger | `name`, `log_file`, `level` | Logger object |

### Configuration

Configuration utilities.

**Location**: `app/utils/config.py`

#### Functions:

| Function | Description | Parameters | Return Value |
|----------|-------------|------------|--------------|
| `load_yaml_config()` | Loads YAML config | `file_path` | Dict: Config data |

## Environment Variables

The following environment variables are used:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LINKEDIN_EMAIL` | LinkedIn email | - | Yes |
| `LINKEDIN_PASSWORD` | LinkedIn password | - | Yes |
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `HEADLESS` | Headless browser mode | `"false"` | No |
| `LINKEDIN_AGENT_LLM` | LLM model | `"openai/gpt-3.5-turbo"` | No |

## File Structure

```
app/
├── agents/
│   ├── agents.py           # Agent initialization
│   ├── tasks.py            # Task initialization
│   └── config/
│       ├── agents.yaml     # Agent configuration
│       └── tasks.yaml      # Task configuration
├── tools/
│   ├── linkedin.py         # LinkedIn browser automation
│   └── linkedin_tools.py   # Message analysis functions
└── utils/
    ├── config.py           # Configuration utilities
    └── logger.py           # Logging utilities
```

## Error Types

| Exception | Description | When Thrown |
|-----------|-------------|-------------|
| `LoginError` | LinkedIn login failed | During login attempt |
| `NavigationError` | Failed to navigate to messages | During page navigation |
| `ExtractionError` | Failed to extract messages | During message extraction |
| `AnalysisError` | Failed to analyze messages | During AI analysis |

## Return Object Formats

### Messages Object

```python
[
    {
        'contact': str,          # Contact name
        'messages': [
            {
                'sender': str,   # Message sender
                'content': str,  # Message content
                'timestamp': str # Message timestamp (when available)
            },
            # Additional messages...
        ]
    },
    # Additional conversations...
]
```

### Analysis Result

String containing the analysis results in the format:

```
Contact: [Contact Name]
Message: [Original Message]
Total Messages: [Number of Messages in Conversation]
Potential Answer: [AI-Generated Response]
==================================================
```

## Integration Points

LinkedIn Agent can be integrated with other systems through:

1. Direct import of classes and functions
2. Processing of log output files
3. Extension of the core classes

# Configuration Guide

This document explains how to configure LinkedIn Agent for your specific needs.

## Environment Variables

LinkedIn Agent uses environment variables for configuration. You can set these in a `.env` file or directly in your environment.

### Essential Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LINKEDIN_EMAIL` | Your LinkedIn account email | - | Yes |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | - | Yes |
| `OPENAI_API_KEY` | OpenAI API key for response generation | - | Yes |
| `HEADLESS` | Run browser in headless mode | `"false"` | No |

### Advanced Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LINKEDIN_AGENT_LLM` | LLM model to use | `"openai/gpt-3.5-turbo"` | No |

## Configuration Files

### YAML Configuration

LinkedIn Agent uses YAML files to configure its AI agents and tasks. These files are located in:

- `app/agents/config/agents.yaml`: Configure agent properties
- `app/agents/config/tasks.yaml`: Configure task properties

#### Agent Configuration Example

```yaml
linkedin_analyst:
  role: >
    LinkedIn Message Analyst
  goal: >
    Analyze LinkedIn messages and suggest appropriate responses
  backstory: >
    I am an automated agent designed to access LinkedIn messages, login to an account,
    analyze conversations, and suggest thoughtful responses based on the message context.
  llm: openai/gpt-3.5-turbo
```

#### Task Configuration Example

```yaml
message_analysis_task:
  description: >
    Access LinkedIn messages, extract the latest conversations, 
    and suggest appropriate responses for each message based 
    on context and professional etiquette.
  expected_output: >
    A list of message response suggestions for each LinkedIn conversation
    that are contextually appropriate and maintain professional tone.
```

## Browser and Driver Configuration

The application automatically handles ChromeDriver installation via the `webdriver_manager` package. However, you can configure some aspects:

- Chrome browser must be installed on your system
- The application will create a `.drivers` directory to store the ChromeDriver
- If you encounter issues with ChromeDriver, see the [Troubleshooting](./troubleshooting.md) guide

## Logging Configuration

Logs are stored in the following locations:

- `logs/linkedin_log_*.txt`: Browser operation logs, login information, and message extraction details
- `logs/message_analysis/analysis_*.txt`: AI analysis and response suggestions

You can configure logging behavior in `app/utils/logger.py` if needed.

# Getting Started with LinkedIn Agent

This guide will help you set up and run LinkedIn Agent for the first time.

## Prerequisites

Before you begin, make sure you have:

- Python 3.8 or higher
- Google Chrome browser installed
- A LinkedIn account
- OpenAI API key (for the AI response generation)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/fabricio-entringer/linkedin-agent.git
cd linkedin-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# Browser Configuration
HEADLESS=false  # Set to "true" to run browser in headless mode
```

> ⚠️ **Security Warning**: Never commit your `.env` file to version control. The `.gitignore` file already excludes this file, but always be cautious.

### 5. Run the Application

```bash
python main.py
```

## What Happens Next

When you run the application:

1. It will launch a Chrome browser (visible or headless, based on your configuration)
2. Log into your LinkedIn account
3. Navigate to your messages
4. Extract the latest conversations
5. Analyze them using AI
6. Generate response suggestions
7. Output the results to the console and log files

Check the logs folder for detailed outputs:
- `logs/linkedin_log_*.txt`: Contains browser and extraction logs
- `logs/message_analysis/analysis_*.txt`: Contains the generated responses

## Next Steps

- Read the [Configuration](./configuration.md) guide to customize your setup
- Check the [Usage Guide](./usage-guide.md) for day-to-day usage tips
- If you encounter issues, refer to the [Troubleshooting](./troubleshooting.md) guide

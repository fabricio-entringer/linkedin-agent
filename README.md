# LinkedIn Automation Agent

A Python application that automates LinkedIn interactions using CrewAI and Selenium. This tool can log in to LinkedIn, navigate to the feed, and extract content.

## Features

- Automated LinkedIn login
- Feed content extraction and logging
- Agent-based automation using CrewAI
- Configurable browser options (headless mode)

## Requirements

- Python 3.8+
- Chrome browser
- OpenAI API key (for CrewAI agents)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd linkedin-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your LinkedIn credentials and OpenAI API key
   ```bash
   cp .env.example .env
   # Then edit .env with your preferred text editor
   ```

## Usage

Run the main script:

```bash
python main.py
```

The application will:
1. Start a Chrome browser
2. Log in to LinkedIn using the credentials in your `.env` file
3. Navigate to the LinkedIn feed
4. Extract content from the feed
5. Save the extracted content to the `logs` directory

## Configuration

Edit the `.env` file to configure:

- LinkedIn credentials
- OpenAI API key
- Browser headless mode

## Project Structure

```
├── app/
│   ├── agents/        # CrewAI agents
│   ├── tools/         # Selenium browser and LinkedIn tools
│   └── utils/         # Utilities and configuration
├── logs/              # Log output directory
├── main.py            # Main application script
├── requirements.txt   # Project dependencies
└── .env               # Environment variables (create from .env.example)
```

## Safety & Ethics

This tool is for educational purposes only. Be aware that:
- Automated scraping may violate LinkedIn's Terms of Service
- Respect rate limits and use responsibly
- Do not use this tool for spamming or data harvesting

## License

MIT

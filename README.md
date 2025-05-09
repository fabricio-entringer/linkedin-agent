# LinkedIn Message Assistant

An automated tool that logs into LinkedIn, analyzes your recent messages, and generates intelligent response suggestions. Built with Python, CrewAI, and Selenium, it helps you craft professional and context-appropriate replies while respecting platform security with single login attempts.

## Features

- Automated LinkedIn login and messaging navigation
- Message extraction and intelligent analysis
- AI-powered contextual response suggestions
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
1. Start a browser instance
2. Log in to LinkedIn using the credentials in your .env file
3. Navigate to the messaging section
4. Extract the latest 5 conversations
5. Generate AI-powered response suggestions for each message
6. Save the analysis with Contact, Message, and Potential Answer to log files

Analysis logs can be found in the `app/logs/message_analysis` directory.

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

## Development Workflow

### Branch Naming Convention

This project follows a standardized branch naming convention to maintain a clean and organized repository. When creating a new branch, please follow this pattern:

```
<type>/<description>
```

#### Branch Types

- `feature/` - For new features or enhancements
- `bugfix/` - For fixing non-critical bugs
- `hotfix/` - For urgent production fixes
- `release/` - For preparing release branches
- `chore/` - For maintenance tasks (e.g., updating dependencies, configs)
- `refactor/` - For code improvements without changing behavior
- `docs/` - For documentation updates only

#### Description Guidelines

The description part should:
- Use lowercase letters, numbers, dashes (-), underscores (_), or dots (.)
- Be concise but descriptive
- Use dashes (-) instead of spaces

#### Examples

```
feature/add-login-api
bugfix/fix-user-profile
hotfix/security-patch
release/v1.2.0
chore/update-dependencies
refactor/clean-auth-service
docs/update-installation-guide
```

#### Protected Branches

⚠️ **IMPORTANT**: Direct pushing to the following branches is not allowed:
- `master` - Main production branch
- `develop` - Development integration branch

All changes to these protected branches must go through Pull Requests with proper code review.

## Safety & Ethics

This tool is for educational purposes only. Be aware that:
- Automated scraping may violate LinkedIn's Terms of Service
- Respect rate limits and use responsibly
- Do not use this tool for spamming or data harvesting

## License

MIT

# Usage Guide

This guide explains how to use LinkedIn Agent effectively for daily operations.

## Basic Usage

The simplest way to use LinkedIn Agent is to run the main script:

```bash
python main.py
```

This will:
1. Start a browser session
2. Log into your LinkedIn account
3. Extract the latest messages
4. Generate AI response suggestions
5. Output the results to the console and log files

## Customizing the Number of Messages

By default, LinkedIn Agent will extract the 5 most recent conversations. You can modify this by editing the `main.py` file and changing the `limit` parameter in the `extract_messages` method call:

```python
# Extract 10 messages instead of the default 5
messages = linkedin_tool.extract_messages(limit=10)
```

## Viewing Generated Responses

After running the tool, AI-generated response suggestions are available in two places:

1. **Console Output**: The responses are printed to the console
2. **Log Files**: The responses are saved in `logs/message_analysis/analysis_*.txt`

Each response includes:
- The contact name
- The original message
- A suggested response

Example output:
```
Contact: John Smith
Message: Hey, do you have time to discuss the project this week?
Total Messages: 1
Potential Answer: Hi John, 

Yes, I'd be happy to discuss the project. I have some availability on Thursday and Friday. What time works best for you?

Best regards,
[Your Name]
==================================================
```

## Running in Headless Mode

For automated environments or to run LinkedIn Agent without showing a browser window, set the `HEADLESS` environment variable to `"true"`:

```bash
# In your .env file
HEADLESS=true
```

Or run it directly:

```bash
HEADLESS=true python main.py
```

## Integrating with Other Systems

LinkedIn Agent can be imported and used as a module in your own Python scripts:

```python
from app.tools.linkedin import LinkedInTool
from app.tools.linkedin_tools import analyze_linkedin_messages

# Initialize the tool
linkedin_tool = LinkedInTool()
linkedin_tool.start()

# Login and extract messages
if linkedin_tool.login():
    if linkedin_tool.go_to_messages():
        messages = linkedin_tool.extract_messages()
        
        # Analyze messages and get response suggestions
        if messages:
            analysis_results = analyze_linkedin_messages(messages)
            print(analysis_results)
            
    # Always close the browser when done
    linkedin_tool.close()
```

## Best Practices

1. **Run Regularly**: For best results, run LinkedIn Agent regularly to stay on top of conversations.
2. **Review Suggestions**: Always review AI-generated suggestions before using them in actual responses.
3. **Update Credentials**: If you change your LinkedIn password, update it in your `.env` file.
4. **Monitor Logs**: Check the logs periodically for any issues or warnings.
5. **Respect LinkedIn's Terms**: Do not use this tool for scraping or automation that violates LinkedIn's terms of service.

# Troubleshooting Guide

This guide helps you diagnose and fix common issues with LinkedIn Agent.

## Login Issues

### Problem: "Unable to login to LinkedIn"

**Possible causes:**
- Incorrect credentials in `.env` file
- LinkedIn security measures (CAPTCHA or verification)
- Network connectivity issues
- Browser compatibility problems

**Solutions:**
1. Verify your LinkedIn credentials in the `.env` file
2. Try running in visible mode (`HEADLESS=false`) to see if there's a CAPTCHA
3. Log in manually in your regular browser to check for security verification requirements
4. Check your internet connection

### Problem: "LinkedIn is requiring verification"

**Solutions:**
1. Log in manually to your LinkedIn account using your regular browser
2. Complete any security verification steps LinkedIn requires
3. Once verified, try running LinkedIn Agent again

## Browser and Driver Issues

### Problem: "ChromeDriver not found" or driver compatibility issues

**Solutions:**
1. Make sure Chrome is installed on your system
2. Allow the application to download the correct driver version automatically:
   ```bash
   # Run once to ensure the driver is downloaded
   python -c "from selenium import webdriver; from webdriver_manager.chrome import ChromeDriverManager; webdriver.Chrome(ChromeDriverManager().install())"
   ```
3. Clear the `.drivers` directory and try again:
   ```bash
   rm -rf .drivers
   ```

### Problem: Browser crashes or freezes

**Solutions:**
1. Update Chrome to the latest version
2. Try running without headless mode:
   ```
   # In .env
   HEADLESS=false
   ```
3. Increase the timeout values in `app/tools/linkedin.py`:
   ```python
   self.wait = WebDriverWait(self.driver, 20)  # Increase from default
   ```

## Message Extraction Issues

### Problem: "No messages found" or "Failed to extract messages"

**Possible causes:**
- LinkedIn UI changes
- Slow network connection
- Missing permissions or restricted account

**Solutions:**
1. Check if LinkedIn has updated its UI (might require selector updates)
2. Increase wait times in the code:
   ```python
   # In app/tools/linkedin.py
   time.sleep(5)  # Increase wait time before extraction
   ```
3. Verify that your account has access to messages (not restricted)
4. Check the logs for specific XPath or selector errors

### Problem: Messages are incomplete or missing

**Solutions:**
1. Scroll through conversations manually before extraction:
   ```python
   # Add to extract_messages method
   self.driver.execute_script("arguments[0].scrollIntoView();", message_element)
   time.sleep(1)  # Wait for content to load
   ```
2. Reduce the number of messages to extract:
   ```python
   messages = linkedin_tool.extract_messages(limit=3)  # Try a smaller number
   ```

## AI Response Generation Issues

### Problem: "OpenAI API Error" or "Failed to generate responses"

**Solutions:**
1. Verify your OpenAI API key in the `.env` file
2. Check your OpenAI account for billing or quota issues
3. Verify network connectivity to OpenAI servers
4. Check if the messages are in a supported language

### Problem: Responses are low quality or inappropriate

**Solutions:**
1. Upgrade to a more capable model:
   ```
   # In .env
   LINKEDIN_AGENT_LLM=openai/gpt-4
   ```
2. Modify the agent prompts in `app/agents/config/agents.yaml` to provide more specific instructions
3. Ensure the extracted messages have enough context (conversation history)

## Log File Issues

### Problem: Cannot find or access log files

**Solutions:**
1. Make sure the `logs` directory exists and is writable:
   ```bash
   mkdir -p logs/message_analysis
   chmod 755 logs logs/message_analysis
   ```
2. Check the logger configuration in `app/utils/logger.py`
3. Run the application with admin/sudo privileges if necessary

## Common Error Messages and Solutions

| Error Message | Potential Solution |
|---------------|-------------------|
| `WebDriverException: Message: unknown error: Chrome failed to start: crashed` | Update Chrome or try without headless mode |
| `NoSuchElementException: Message: no such element: Unable to locate element` | LinkedIn UI may have changed, update the XPath selectors |
| `TimeoutException: Message: timeout: Timed out receiving message from renderer` | Increase timeout values or check internet connection |
| `InvalidSessionIdException: Message: invalid session id` | Browser session was terminated, check for memory issues |
| `AuthenticationError: Incorrect API key provided` | Check your OpenAI API key in .env |

## Getting Additional Help

If you continue to experience issues:

1. Check the detailed logs in the `logs` directory
2. Open an issue on the GitHub repository with:
   - Detailed description of the problem
   - Steps to reproduce
   - Log file contents (with sensitive information removed)
   - Your environment (OS, Python version, Chrome version)
3. Try running with verbose logging enabled:
   ```python
   # Add to main.py before creating LinkedInTool
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

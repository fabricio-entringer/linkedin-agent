# Conversation Extraction

This guide explains how LinkedIn Agent extracts and processes conversations from LinkedIn.

## How Conversation Extraction Works

LinkedIn Agent uses a Selenium-based approach to extract messages from your LinkedIn inbox:

1. **Login Process**: The tool logs in to LinkedIn using your credentials
2. **Navigation**: It navigates to the messaging section of LinkedIn
3. **Message Selection**: It identifies and selects the most recent conversations
4. **Data Extraction**: For each conversation, it extracts:
   - Contact name
   - Message content
   - Timestamp (when available)
   - Conversation history (preceding messages)

## Extraction Process Details

### Browser Automation

The tool uses Chrome browser automation via Selenium to interact with LinkedIn's web interface. The browser can run in:

- **Visible mode** (default): You can see the browser actions in real-time
- **Headless mode**: Browser runs in the background (set `HEADLESS=true` in your `.env`)

### Element Selection

LinkedIn Agent uses a combination of XPath and CSS selectors to identify and extract message elements from the page. These selectors are defined in the `app/tools/linkedin.py` file.

### Conversation Limits

By default, the tool extracts the 5 most recent conversations. You can modify this limit by changing the `extract_messages` parameter:

```python
# Extract 10 conversations instead of 5
messages = linkedin_tool.extract_messages(limit=10)
```

### Data Structure

Extracted conversations are structured as follows:

```python
{
    'contact': 'Contact Name',
    'messages': [
        {'sender': 'Contact Name', 'content': 'Message content', 'timestamp': 'timestamp'},
        {'sender': 'You', 'content': 'Your reply', 'timestamp': 'timestamp'},
        # Additional messages...
    ]
}
```

## Limitations

1. **Rate Limiting**: Excessive use may trigger LinkedIn's rate limiting or security measures
2. **UI Changes**: LinkedIn UI changes might affect the selectors, requiring updates
3. **Message Count**: Only the most recent messages in each conversation are extracted
4. **Media Content**: Images, files, and other non-text content are not processed

## Customizing Extraction

### Modifying XPath Selectors

If LinkedIn changes its UI and the selectors need updating, you can modify them in `app/tools/linkedin.py`:

```python
# Example of updating a selector
self.message_list_selector = "//div[@class='new-selector-path']"
```

### Extending Functionality

To extract additional data from conversations, you can extend the `extract_messages` method in the `LinkedInTool` class:

```python
def extract_messages(self, limit=5):
    # Existing code...
    
    # Extract additional data
    additional_data = element.find_element(By.XPATH, "//path/to/element").text
    
    # Add to the message structure
    messages_data.append({
        # Existing fields...
        'additional_data': additional_data
    })
    
    # Rest of the method...
```

## Error Handling

The extraction process includes error handling for common issues:

- **Login Failures**: Detected and reported with detailed error messages
- **Navigation Issues**: Timeout handling with configurable wait times
- **Element Not Found**: Graceful error handling when elements cannot be located

See the [Troubleshooting](./troubleshooting.md) guide for solutions to common extraction issues.

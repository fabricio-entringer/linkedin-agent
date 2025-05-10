import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from app.tools.browser import BrowserTool
from app.utils.logger import logger, log_content
from app.utils.config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD

class LinkedInTool:
    """A tool for interacting with LinkedIn"""
    
    def __init__(self):
        self.browser = BrowserTool()
        self.logged_in = False
    
    def start(self):
        """Start the browser"""
        return self.browser.start_browser()
    
    def login(self):
        """Log in to LinkedIn"""
        if self.logged_in:
            logger.info("Already logged in to LinkedIn")
            return True
        
        if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
            logger.error("LinkedIn credentials not set in environment variables")
            return False
        
        logger.info("Logging in to LinkedIn...")
        
        # Navigate to LinkedIn login page
        if not self.browser.navigate_to("https://www.linkedin.com/login"):
            return False
        
        # Input email
        if not self.browser.send_keys("#username", LINKEDIN_EMAIL):
            return False
        
        # Input password
        if not self.browser.send_keys("#password", LINKEDIN_PASSWORD):
            return False
        
        # Click the login button
        if not self.browser.wait_and_click("button[type='submit']"):
            return False
        
        # Wait for the login to complete - LinkedIn might take longer due to security checks
        self.browser.sleep(5)
        
        # Check if login was successful
        try:
            # Look for elements that would indicate successful login - try multiple selectors
            success_selectors = [
                ".global-nav__me-photo",  # Profile icon
                ".feed-identity-module__member-photo",  # Another possible profile icon
                ".feed-container",  # Feed container
                ".search-global-typeahead__input"  # Search bar
            ]
            
            for selector in success_selectors:
                logger.info(f"Checking for login success with selector: {selector}")
                element = self.browser.wait_for_element(selector, timeout=10)
                if element:
                    self.logged_in = True
                    logger.info(f"Successfully logged in to LinkedIn (detected {selector})")
                    return True
            
            # Check for security challenges or verification pages
            challenge_selectors = [
                ".challenge-dialog",  # Security verification
                "#captcha-challenge",  # CAPTCHA
                ".pin-verification"   # PIN verification
            ]
            
            for selector in challenge_selectors:
                element = self.browser.find_element(selector)
                if element:
                    logger.error(f"LinkedIn is requesting additional verification: {selector}")
                    return False
            
            logger.error("Failed to log in to LinkedIn - could not verify successful login")
            return False
        except Exception as e:
            logger.error(f"Error during login verification: {e}")
            return False
    
    def go_to_messages(self):
        """Navigate to the LinkedIn messaging page"""
        if not self.logged_in:
            logger.error("Not logged in to LinkedIn. Cannot navigate to messages.")
            return False
        
        logger.info("Navigating to LinkedIn messages...")
        return self.browser.navigate_to("https://www.linkedin.com/messaging/")
    
    def extract_messages(self, limit=5):
        """Extract the latest messages from LinkedIn chats
        
        Args:
            limit (int): Maximum number of messages to extract
            
        Returns:
            list: List of dictionaries with conversation data in format:
                 {'contact': name, 'messages': [{'sender': name, 'content': text, 'timestamp': time}], 'message_count': count}
        """
        if not self.logged_in:
            logger.error("Not logged in to LinkedIn. Cannot extract messages.")
            return False
        
        logger.info(f"Extracting the latest {limit} messages from LinkedIn chats...")
        
        # Wait for the messaging UI to load
        self.browser.sleep(3)
        
        # Get the page source and parse with BeautifulSoup
        page_source = self.browser.get_page_source()
        soup = BeautifulSoup(page_source, 'html.parser')
        
        try:
            messages_content = []
            
            # Try to find conversation list - we need to try multiple selectors as LinkedIn's UI might change
            conversations = soup.find_all("li", {"class": "msg-conversation-card"})
            
            if not conversations:
                # Try another selector if the first one doesn't work
                conversations = soup.find_all("div", {"class": "msg-conversation-card__content"})
                
            if not conversations:
                # Try more generic selectors
                conversations = soup.find_all("div", {"class": "msg-conversation-listitem__link"})
                    
                if not conversations:
                    # As a fallback, look for any elements that might contain messaging content
                    conversations = soup.find_all("div", {"data-control-name": "overlay.expand_conversation"})
            
            # Process up to the limit
            for idx, conversation in enumerate(conversations[:limit]):
                contact_name = "Unknown Contact"
                
                # Extract contact name - try multiple selectors
                name_elem = conversation.find("h3", {"class": "msg-conversation-card__participant-names"})
                if not name_elem:
                    name_elem = conversation.find("span", {"class": "msg-conversation-listitem__participant-names"})
                if not name_elem:
                    name_elem = conversation.find("span", {"class": "t-16"})
                if name_elem:
                    contact_name = name_elem.get_text(strip=True)
                
                logger.info(f"Processing conversation with: {contact_name}")
                
                # Find the clickable element to open the conversation
                conversation_elem = None
                
                # Try to find the conversation element in the DOM using Selenium
                try:
                    # Different selectors LinkedIn might use
                    selectors = [
                        f"//h3[contains(text(), '{contact_name}')]/ancestor::li",
                        f"//span[contains(text(), '{contact_name}')]/ancestor::div[contains(@class, 'msg-conversation-card')]",
                        f"//span[contains(text(), '{contact_name}')]/ancestor::div[contains(@class, 'msg-conversation-listitem__link')]"
                    ]
                    
                    for selector in selectors:
                        try:
                            conversation_elem = self.browser.find_element_by_xpath(selector)
                            if conversation_elem:
                                break
                        except:
                            continue
                            
                    if not conversation_elem:
                        logger.warning(f"Could not find clickable element for conversation with {contact_name}")
                        continue
                        
                    # Click on the conversation to open it
                    logger.info(f"Opening conversation with {contact_name}")
                    self.browser.click_element(conversation_elem)
                    
                    # Wait for the conversation to load
                    self.browser.sleep(2)
                    
                    # Extract all messages in the conversation
                    conversation_messages = []
                    
                    # Get updated page source after clicking
                    conversation_page = self.browser.get_page_source()
                    conversation_soup = BeautifulSoup(conversation_page, 'html.parser')
                    
                    # Find the message container
                    message_container = conversation_soup.find("div", {"class": "msg-conversation-list-content"})
                    if not message_container:
                        message_container = conversation_soup.find("div", {"class": "msg-s-message-list-container"})
                    
                    if message_container:
                        # Find all message items
                        message_items = message_container.find_all("li", {"class": "msg-s-message-list__event"})
                        if not message_items:
                            # Try alternative selectors
                            message_items = message_container.find_all("div", {"class": "msg-s-message-group"})
                            
                        for message_item in message_items:
                            sender = "Unknown"
                            content = "No content"
                            timestamp = ""
                            
                            # Extract sender
                            sender_elem = message_item.find("span", {"class": "msg-s-message-group__name"})
                            if not sender_elem:
                                sender_elem = message_item.find("span", {"class": "profile-card__name"})
                            if sender_elem:
                                sender = sender_elem.get_text(strip=True)
                            else:
                                # If no sender found, check if it's from the user ("You")
                                if message_item.find("div", {"class": "msg-s-message-group--from-participant"}):
                                    sender = contact_name
                                else:
                                    sender = "You"
                                    
                            # Extract message content
                            content_elem = message_item.find("p", {"class": "msg-s-event-listitem__body"})
                            if not content_elem:
                                content_elem = message_item.find("div", {"class": "msg-s-event__content"})
                            if not content_elem:
                                content_elem = message_item.find("p")
                            if content_elem:
                                content = content_elem.get_text(strip=True)
                                
                            # Extract timestamp if available
                            timestamp_elem = message_item.find("time")
                            if timestamp_elem:
                                timestamp = timestamp_elem.get_text(strip=True)
                                
                            # Add message to the conversation
                            conversation_messages.append({
                                "sender": sender,
                                "content": content, 
                                "timestamp": timestamp
                            })
                    
                    # Add the conversation to our results
                    message_count = len(conversation_messages)
                    
                    if message_count == 0:
                        # If we couldn't extract structured messages, at least get the last message preview
                        msg_elem = conversation.find("span", {"class": "msg-conversation-card__message-snippet-body"})
                        if not msg_elem:
                            msg_elem = conversation.find("div", {"class": "msg-conversation-card__message-snippet"})
                        if not msg_elem:
                            msg_elem = conversation.find("p", {"class": "mail-messages-list__body"})
                        if msg_elem:
                            last_message = msg_elem.get_text(strip=True)
                            conversation_messages.append({
                                "sender": "Unknown",
                                "content": last_message,
                                "timestamp": ""
                            })
                            message_count = 1
                    
                    messages_content.append({
                        "contact": contact_name,
                        "messages": conversation_messages,
                        "message_count": message_count
                    })
                    
                    # Navigate back to the messages list
                    # Locate and click on the back button or click on the messages navigation item
                    back_button = self.browser.find_element_by_xpath("//button[contains(@class, 'msg-overlay-bubble-header__back-button')]")
                    if back_button:
                        self.browser.click_element(back_button)
                        self.browser.sleep(1)
                    else:
                        # Alternative: click on messaging icon in the nav
                        messaging_nav = self.browser.find_element_by_xpath("//a[contains(@href, '/messaging')]")
                        if messaging_nav:
                            self.browser.click_element(messaging_nav)
                            self.browser.sleep(2)
                            
                except Exception as e:
                    logger.error(f"Error processing conversation with {contact_name}: {e}")
                    # Try to navigate back to messages list
                    self.browser.navigate_to("https://www.linkedin.com/messaging/")
                    self.browser.sleep(2)
                    continue
            
            if messages_content:
                # Format content for logging
                formatted_content = "\n\n".join([
                    f"Contact: {msg['contact']}\n" +
                    f"Message Count: {msg['message_count']}\n" +
                    "\n".join([
                        f"- {m['sender']}: {m['content']} ({m['timestamp']})"
                        for m in msg['messages']
                    ]) +
                    f"\n{'=' * 50}"
                    for msg in messages_content
                ])
                
                # Log the extracted content
                log_content(formatted_content, "linkedin_messages")
                logger.info(f"Extracted {len(messages_content)} conversations with a total of {sum(msg['message_count'] for msg in messages_content)} messages")
                
                return messages_content
            else:
                logger.warning("No messages found in LinkedIn chats")
                return []
                
        except Exception as e:
            logger.error(f"Error extracting messages: {e}")
            return []
    
    def close(self):
        """Close the browser"""
        return self.browser.close()

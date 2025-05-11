import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from app.tools.browser import BrowserTool
from app.tools.linkedin_base import LinkedInChatExtractor
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
                 {'contact': name, 'messages': [list_of_messages], 'message_count': count}
        """
        if not self.logged_in:
            logger.error("Not logged in to LinkedIn. Cannot extract messages.")
            return False
        
        logger.info(f"Extracting the latest {limit} messages from LinkedIn chats...")
        
        # Wait for the messaging UI to load
        self.browser.sleep(5)
        
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
                last_message = "No message content"
                
                # Extract contact name - try multiple selectors
                name_elem = conversation.find("h3", {"class": "msg-conversation-card__participant-names"})
                if not name_elem:
                    name_elem = conversation.find("span", {"class": "msg-conversation-listitem__participant-names"})
                if not name_elem:
                    name_elem = conversation.find("span", {"class": "t-16"})
                if name_elem:
                    contact_name = name_elem.get_text(strip=True)
                
                # Extract last message - try multiple selectors
                msg_elem = conversation.find("span", {"class": "msg-conversation-card__message-snippet-body"})
                if not msg_elem:
                    msg_elem = conversation.find("div", {"class": "msg-conversation-card__message-snippet"})
                if not msg_elem:
                    msg_elem = conversation.find("p", {"class": "mail-messages-list__body"})
                if not msg_elem:
                    # Last resort - find any element that might contain message text
                    msg_elem = conversation.find("div", class_=lambda c: c and "message" in c.lower())
                if msg_elem:
                    last_message = msg_elem.get_text(strip=True)
                
                # Add to our results with the new structure
                messages_content.append({
                    "contact": contact_name,
                    "messages": [last_message],  # For now, just include the last message in the list
                    "message_count": 1
                })

            if messages_content:
                # Format content for logging
                formatted_content = "\n\n".join([
                    f"Contact: {msg['contact']}\n"
                    f"Message: {msg['messages'][0]}\n"  # Display the first message for logging
                    f"Message Count: {msg['message_count']}\n"
                    f"{'=' * 50}"
                    for msg in messages_content
                ])
                
                # Log the extracted content
                log_content(formatted_content, "linkedin_messages")
                logger.info(f"Extracted {len(messages_content)} conversations from LinkedIn")
                
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



    def extract_messages_full(self, limit=5):
        """Extract the latest messages from LinkedIn chats
        
        Args:
            limit (int): Maximum number of messages to extract
            
        Returns:
            list: List of dictionaries with conversation data in format:
                 {'contact': name, 'messages': [list_of_messages], 'message_count': count}
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
            conversations = soup.find_all("li", {"class": "msg-conversation-listitem"})
            
            # Process up to the limit
            for idx, conversation in enumerate(conversations[:limit]):
                contact_name = "Unknown Contact"
                last_message = "No message content"
                
                # Extract contact name - try multiple selectors
                name_elem = conversation.find("h3", {"class": "msg-conversation-card__participant-names"})
                if not name_elem:
                    name_elem = conversation.find("span", {"class": "msg-conversation-listitem__participant-names"})
                if not name_elem:
                    name_elem = conversation.find("span", {"class": "t-16"})
                if name_elem:
                    contact_name = name_elem.get_text(strip=True)
                
                # Extract last message - try multiple selectors
                msg_elem = conversation.find("span", {"class": "msg-conversation-card__message-snippet-body"})
                if not msg_elem:
                    msg_elem = conversation.find("div", {"class": "msg-conversation-card__message-snippet"})
                if not msg_elem:
                    msg_elem = conversation.find("p", {"class": "mail-messages-list__body"})
                if not msg_elem:
                    # Last resort - find any element that might contain message text
                    msg_elem = conversation.find("div", class_=lambda c: c and "message" in c.lower())
                if msg_elem:
                    last_message = msg_elem.get_text(strip=True)
                
                # Add to our results with the new structure
                messages_content.append({
                    "contact": contact_name,
                    "last_message": last_message,
                    "message_count": 1,
                    "messages": []
                })
            
            print("*********************************************")
            print(f"Messages: {messages_content}")
            print("*********************************************")
            

            # Click on the conversation to load messages
            for idx, message in enumerate(messages_content):


                # Find the specific conversation element by matching contact name
                logger.info(f"Looking for conversation with {message['contact']}...")

                # First find all conversation list items
                list_items = self.browser.driver.find_elements(By.XPATH, "//div[contains(@class, 'msg-conversation-listitem__link')]")


                # Then iterate through them to find the one with the matching contact name
                for item in list_items:
                    try:
                        print(f"Checking list item: {item.text}")
                        print("*****************************************************************")
                        span_text = item.text
                        if message['contact'] in span_text:
                            # Found the right conversation
                            item.click()
                            logger.info(f"Clicked on conversation with {message['contact']}")
                            self.browser.sleep(5)

                            # full_message_div = self.browser.driver.find_element(By.XPATH, "//div[contains(@class, 'msg-thread')]")

                            # #Get the li element with class = msg-s-message-list__event
                            # event_elements = full_message_div.find_elements(By.XPATH, "//li[contains(@class, 'msg-s-message-list__event')]")

                            # for event in event_elements:
                            #     message_text = event.find_element(By.XPATH, ".//span[contains(@class, 'msg-s-message-list__event-text')]").text
                            #     message_time = event.find_element(By.XPATH, ".//span[contains(@class, 'msg-s-message-list__event-time')]").text
                            #     message_sender = event.find_element(By.XPATH, ".//span[contains(@class, 'msg-s-message-list__event-sender')]").text
                            #     message = {
                            #         "text": message_text,
                            #         "time": message_time,
                            #         "sender": message_sender
                            #     }
                            #     messages.append(message)

                            extractor = LinkedInChatExtractor()
                            result = extractor.extract_chat_from_html(self.browser.get_page_source())
                            print("*********************************************")
                            print(f" ")
                            print(f"Result: {result}")
                            print(f" ")
                            print("*********************************************")

                            break
                    except Exception as e:
                        logger.debug(f"Error checking list item: {e}")



            messages_content = []

            if messages_content:
                # Format content for logging
                formatted_content = "\n\n".join([
                    f"Contact: {msg['contact']}\n"
                    f"Message: {msg['last_message']}\n"  # Display the last message for logging
                    f"Message Count: {len(msg['messages'])}\n"
                    f"{'=' * 50}"
                    for msg in messages_content
                ])
                
                # Log the extracted content
                log_content(formatted_content, "linkedin_messages")
                logger.info(f"Extracted {len(messages_content)} conversations from LinkedIn")
                
                return messages_content
            else:
                logger.warning("No messages found in LinkedIn chats")
                return []
                
        except Exception as e:
            logger.error(f"Error extracting messages: {e}")
            return []
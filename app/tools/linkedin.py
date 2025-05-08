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
        
        # Wait for the login to complete
        self.browser.sleep(3)
        
        # Check if login was successful
        try:
            # Look for elements that would indicate successful login
            profile_icon = self.browser.wait_for_element(".global-nav__me-photo", timeout=5)
            if profile_icon:
                self.logged_in = True
                logger.info("Successfully logged in to LinkedIn")
                return True
            else:
                logger.error("Failed to log in to LinkedIn")
                return False
        except Exception as e:
            logger.error(f"Error during login verification: {e}")
            return False
    
    def go_to_feed(self):
        """Navigate to the LinkedIn feed/home page"""
        if not self.logged_in:
            logger.error("Not logged in to LinkedIn. Cannot navigate to feed.")
            return False
        
        logger.info("Navigating to LinkedIn feed...")
        return self.browser.navigate_to("https://www.linkedin.com/feed/")
    
    def extract_feed_content(self):
        """Extract content from the LinkedIn feed"""
        if not self.logged_in:
            logger.error("Not logged in to LinkedIn. Cannot extract feed content.")
            return False
        
        logger.info("Extracting content from LinkedIn feed...")
        
        # Scroll a few times to load more content
        for _ in range(3):
            self.browser.scroll_down(500)
            self.browser.sleep(1)
        
        # Get the page source and parse with BeautifulSoup
        page_source = self.browser.get_page_source()
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract posts
        try:
            feed_content = []
            
            # Find all feed posts
            posts = soup.find_all("div", {"class": "feed-shared-update-v2"})
            
            if not posts:
                # Try another selector if the first one doesn't work
                posts = soup.find_all("div", {"data-urn": True})
            
            for post in posts:
                post_author = "Unknown"
                post_text = "No content"
                
                # Try to get post author
                author_elem = post.find("span", {"class": "feed-shared-actor__name"})
                if author_elem:
                    post_author = author_elem.get_text(strip=True)
                
                # Try to get post text
                text_elem = post.find("div", {"class": "feed-shared-update-v2__description-wrapper"})
                if text_elem:
                    post_text = text_elem.get_text(strip=True)
                else:
                    # Try alternative selector
                    text_elem = post.find("span", {"class": "break-words"})
                    if text_elem:
                        post_text = text_elem.get_text(strip=True)
                
                feed_content.append({
                    "author": post_author,
                    "text": post_text
                })
            
            if feed_content:
                # Format content for logging
                formatted_content = "\n\n".join([
                    f"Author: {post['author']}\n"
                    f"Text: {post['text']}\n"
                    f"{'=' * 50}"
                    for post in feed_content
                ])
                
                # Log the extracted content
                log_content(formatted_content, "linkedin_feed")
                logger.info(f"Extracted {len(feed_content)} posts from LinkedIn feed")
                
                return formatted_content
            else:
                logger.warning("No posts found in the LinkedIn feed")
                return "No posts found in the feed."
            
        except Exception as e:
            logger.error(f"Error extracting feed content: {e}")
            return f"Error extracting feed content: {str(e)}"
    
    def close(self):
        """Close the browser"""
        return self.browser.close()

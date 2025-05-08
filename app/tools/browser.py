import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from app.utils.logger import logger
from app.utils.config import HEADLESS

class BrowserTool:
    """A tool for managing the web browser using Selenium"""
    
    def __init__(self):
        self.driver = None
        
    def start_browser(self):
        """Initialize and start the Chrome browser"""
        logger.info("Starting browser...")
        
        # Set up Chrome options
        options = Options()
        if HEADLESS:
            options.add_argument('--headless')
        
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize Chrome driver
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
            
            # Mask automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Browser started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            return False
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        if not self.driver:
            logger.error("Browser not started. Call start_browser() first.")
            return False
        
        try:
            logger.info(f"Navigating to URL: {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return False
    
    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=10):
        """Wait for an element to be present on the page"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except TimeoutException:
            logger.error(f"Timed out waiting for element with selector: {selector}")
            return None
    
    def find_element(self, selector, by=By.CSS_SELECTOR):
        """Find an element on the page"""
        try:
            element = self.driver.find_element(by, selector)
            return element
        except NoSuchElementException:
            logger.error(f"Element not found with selector: {selector}")
            return None
    
    def find_elements(self, selector, by=By.CSS_SELECTOR):
        """Find multiple elements on the page"""
        try:
            elements = self.driver.find_elements(by, selector)
            return elements
        except Exception as e:
            logger.error(f"Failed to find elements with selector '{selector}': {e}")
            return []
    
    def wait_and_click(self, selector, by=By.CSS_SELECTOR, timeout=10):
        """Wait for an element and click it when available"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            element.click()
            return True
        except Exception as e:
            logger.error(f"Failed to click element with selector '{selector}': {e}")
            return False
    
    def send_keys(self, selector, text, by=By.CSS_SELECTOR, timeout=10):
        """Type text into an input field"""
        try:
            element = self.wait_for_element(selector, by, timeout)
            if element:
                element.clear()
                element.send_keys(text)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to send keys to element with selector '{selector}': {e}")
            return False
    
    def get_page_source(self):
        """Return the full page source"""
        if not self.driver:
            logger.error("Browser not started. Call start_browser() first.")
            return ""
        
        try:
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Failed to get page source: {e}")
            return ""
    
    def get_element_text(self, selector, by=By.CSS_SELECTOR):
        """Get the text content of an element"""
        element = self.find_element(selector, by)
        if element:
            return element.text
        return ""
    
    def get_all_text(self, selector, by=By.CSS_SELECTOR):
        """Get text from all matching elements"""
        elements = self.find_elements(selector, by)
        return [element.text for element in elements if element.text.strip()]
    
    def scroll_down(self, pixels=300):
        """Scroll down the page by the specified number of pixels"""
        try:
            self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            return True
        except Exception as e:
            logger.error(f"Failed to scroll down: {e}")
            return False
    
    def scroll_to_element(self, element):
        """Scroll to make an element visible"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return True
        except Exception as e:
            logger.error(f"Failed to scroll to element: {e}")
            return False
    
    def sleep(self, seconds):
        """Pause execution for the specified number of seconds"""
        time.sleep(seconds)
    
    def close(self):
        """Close the browser and clean up"""
        if self.driver:
            logger.info("Closing browser...")
            try:
                self.driver.quit()
                self.driver = None
                logger.info("Browser closed successfully")
                return True
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
                return False
        return True

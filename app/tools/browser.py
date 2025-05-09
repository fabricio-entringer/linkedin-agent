import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from app.utils.logger import logger
from app.utils.config import HEADLESS

class BrowserTool:
    """A tool for managing the web browser using Selenium"""
    
    def __init__(self):
        self.driver = None
        
    def _get_chrome_version(self):
        """Get the Chrome browser version installed on the system"""
        import subprocess
        import platform
        import re
        
        try:
            system = platform.system()
            if system == "Linux":
                # Try different commands for Linux
                commands = [
                    ["google-chrome", "--version"],
                    ["google-chrome-stable", "--version"],
                    ["chromium", "--version"],
                    ["chromium-browser", "--version"]
                ]
                
                for cmd in commands:
                    try:
                        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
                        version = re.search(r'\d+\.\d+\.\d+', output)
                        if version:
                            logger.info(f"Detected Chrome version: {version.group(0)}")
                            return version.group(0)
                    except:
                        continue
                        
            elif system == "Darwin":  # macOS
                cmd = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"]
                output = subprocess.check_output(cmd).decode('utf-8')
                version = re.search(r'\d+\.\d+\.\d+', output)
                if version:
                    return version.group(0)
                    
            elif system == "Windows":
                cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
                output = subprocess.check_output(cmd, shell=True).decode('utf-8')
                version = re.search(r'\d+\.\d+\.\d+\.\d+', output)
                if version:
                    return version.group(0)
                    
            logger.warning("Could not detect Chrome version, using default.")
            return None
            
        except Exception as e:
            logger.warning(f"Error detecting Chrome version: {e}")
            return None
        
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
            # Try to detect Chrome version
            chrome_version = self._get_chrome_version()
            
            # Create a local .drivers directory in the project root for driver storage
            import os
            drivers_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".drivers")
            os.makedirs(drivers_dir, exist_ok=True)
            logger.info(f"Using drivers directory: {drivers_dir}")
            
            # Install ChromeDriver with version if available
            if chrome_version:
                logger.info(f"Installing ChromeDriver for Chrome version {chrome_version}")
                driver_path = ChromeDriverManager(version=chrome_version, path=drivers_dir).install()
            else:
                logger.info("Installing latest ChromeDriver")
                driver_path = ChromeDriverManager(path=drivers_dir).install()
                
            logger.info(f"Using ChromeDriver from path: {driver_path}")
            
            # Make sure ChromeDriver is executable
            os.chmod(driver_path, 0o755)
            
            service = Service(executable_path=driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
            
            # Mask automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Browser started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            import os
            import glob
            import subprocess
            
            if "Exec format error" in str(e):
                logger.error("This appears to be an executable permission issue with ChromeDriver")
                try:
                    # Find the correct ChromeDriver executable in the .drivers directory
                    drivers_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".drivers")
                    
                    # Try to find Chrome/Chromium to determine if it's installed
                    try:
                        chrome_check = subprocess.check_output(["which", "google-chrome"]).decode('utf-8').strip()
                        logger.info(f"Chrome found at: {chrome_check}")
                    except:
                        try:
                            chrome_check = subprocess.check_output(["which", "chromium"]).decode('utf-8').strip()
                            logger.info(f"Chromium found at: {chrome_check}")
                        except:
                            logger.error("Could not find Chrome or Chromium browser. Please install it first.")
                            return False
                    
                    # Find all chromedriver executables
                    chromedriver_files = []
                    for root, dirs, files in os.walk(drivers_dir):
                        for file in files:
                            if "chromedriver" in file and not file.endswith("NOTICES") and not file.endswith("zip"):
                                full_path = os.path.join(root, file)
                                chromedriver_files.append(full_path)
                                
                    if chromedriver_files:
                        logger.info(f"Found ChromeDriver candidates: {', '.join(chromedriver_files)}")
                        
                        # Try each chromedriver
                        for driver in chromedriver_files:
                            try:
                                logger.info(f"Attempting to use ChromeDriver at: {driver}")
                                # Fix permissions
                                os.chmod(driver, 0o755)
                                
                                # Try to use this driver
                                service = Service(executable_path=driver)
                                self.driver = webdriver.Chrome(service=service, options=options)
                                self.driver.maximize_window()
                                
                                logger.info(f"Success! Using ChromeDriver: {driver}")
                                return True
                            except Exception as inner_e:
                                logger.error(f"Failed with this driver: {inner_e}")
                                continue
                    
                    # If we're here, none of the existing drivers worked
                    logger.info("Attempting to download ChromeDriver again with different settings")
                    
                    # Try a few different approaches
                    try:
                        # Try using ChromeDriverManager with explicit version
                        from webdriver_manager.chrome import ChromeDriverManager
                        driver_path = ChromeDriverManager(version="latest", path=drivers_dir).install()
                        os.chmod(driver_path, 0o755)
                        
                        service = Service(executable_path=driver_path)
                        self.driver = webdriver.Chrome(service=service, options=options)
                        self.driver.maximize_window()
                        logger.info("Browser started successfully with 'latest' ChromeDriver")
                        return True
                    except Exception as retry_e:
                        logger.error(f"Failed to start with 'latest' version: {retry_e}")
                        
                except Exception as e2:
                    logger.error(f"Failed to fix ChromeDriver issues: {e2}")
            
            # Provide help for different types of errors
            if "DevToolsActivePort file doesn't exist" in str(e):
                logger.error("This may be due to Chrome already running or being used by another process.")
                logger.info("Try adding --no-sandbox flag or running with a non-root user")
            elif "unknown error: cannot find Chrome binary" in str(e):
                logger.error("Chrome browser binary not found. Please install Chrome browser.")
            
            # Try alternative approaches as a last resort
            logger.info("Trying alternative browser setup approaches...")
            return self._try_alternative_browser_setup(options)
    
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
    
    def _try_alternative_browser_setup(self, options):
        """Try alternative browser setup approaches when the main one fails"""
        import os
        import platform
        import subprocess
        
        logger.info("Trying alternative browser setup approaches...")
        
        try:
            # Add platform-specific Chrome binary paths
            system = platform.system()
            if system == "Linux":
                # Check for common Chrome/Chromium paths on Linux
                chrome_paths = [
                    "/usr/bin/google-chrome",
                    "/usr/bin/google-chrome-stable",
                    "/usr/bin/chromium",
                    "/usr/bin/chromium-browser"
                ]
                
                for path in chrome_paths:
                    if os.path.exists(path):
                        logger.info(f"Found Chrome/Chromium at: {path}")
                        options.binary_location = path
                        break
            
            # Try direct ChromeDriver download without using webdriver_manager
            try:
                from selenium.webdriver.chrome.service import Service
                from selenium import webdriver
                
                # Create a temporary directory for ChromeDriver if needed
                chrome_driver_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".chromedriver")
                os.makedirs(chrome_driver_dir, exist_ok=True)
                
                # Use selenium's built-in service
                service = Service()
                self.driver = webdriver.Chrome(service=service, options=options)
                self.driver.maximize_window()
                logger.info("Successfully started browser using Selenium's built-in ChromeDriver service")
                return True
            except Exception as selenium_e:
                logger.error(f"Failed to start with Selenium's built-in service: {selenium_e}")
            
            # Try using a system-installed chromedriver if available
            try:
                chrome_driver_path = None
                try:
                    # Check if chromedriver is in PATH
                    chrome_driver_path = subprocess.check_output(["which", "chromedriver"]).decode('utf-8').strip()
                    logger.info(f"Found system chromedriver at: {chrome_driver_path}")
                except:
                    logger.info("Could not find system chromedriver")
                
                if chrome_driver_path and os.path.exists(chrome_driver_path):
                    service = Service(executable_path=chrome_driver_path)
                    self.driver = webdriver.Chrome(service=service, options=options)
                    self.driver.maximize_window()
                    logger.info("Successfully started browser using system chromedriver")
                    return True
            except Exception as system_e:
                logger.error(f"Failed to start with system chromedriver: {system_e}")
            
            return False
            
        except Exception as e:
            logger.error(f"Failed all alternative browser setup approaches: {e}")
            return False

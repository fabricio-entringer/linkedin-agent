#!/usr/bin/env python3
"""
Utility script to check ChromeDriver installation and compatibility with Chrome.
Run this script to diagnose ChromeDriver issues.
"""

import os
import sys
import platform
import subprocess
import re
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('chromedriver-check')

def get_chrome_version():
    """Get the installed Chrome/Chromium version"""
    system = platform.system()
    try:
        if system == "Linux":
            commands = [
                ["google-chrome", "--version"],
                ["google-chrome-stable", "--version"],
                ["chromium", "--version"],
                ["chromium-browser", "--version"]
            ]
            
            for cmd in commands:
                try:
                    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
                    logger.info(f"Command output: {output.strip()}")
                    version = re.search(r'\d+\.\d+\.\d+', output)
                    if version:
                        return version.group(0)
                except Exception as e:
                    logger.debug(f"Command {cmd} failed: {e}")
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
                
        logger.warning("Could not detect Chrome version.")
        return None
        
    except Exception as e:
        logger.error(f"Error detecting Chrome version: {e}")
        return None

def find_chrome_binary():
    """Find Chrome/Chromium binary path"""
    system = platform.system()
    possible_paths = []
    
    if system == "Linux":
        possible_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium"
        ]
    elif system == "Darwin":  # macOS
        possible_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium"
        ]
    elif system == "Windows":
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv("USERNAME"))
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Found Chrome/Chromium binary at: {path}")
            return path
    
    logger.warning("Could not find Chrome/Chromium binary")
    return None

def test_selenium_setup():
    """Test if Selenium can set up and use ChromeDriver"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        logger.info("Selenium is installed")
        
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            logger.info("webdriver_manager is installed")
            
            # Create a local directory for testing
            test_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".test_drivers")
            os.makedirs(test_dir, exist_ok=True)
            
            # Try to install ChromeDriver
            try:
                logger.info("Attempting to install ChromeDriver...")
                driver_path = ChromeDriverManager(path=test_dir).install()
                logger.info(f"ChromeDriver installed at: {driver_path}")
                
                # Make sure the file is executable
                os.chmod(driver_path, 0o755)
                
                # Check if the file is executable
                if not os.access(driver_path, os.X_OK):
                    logger.error(f"ChromeDriver at {driver_path} is not executable!")
                else:
                    logger.info(f"ChromeDriver at {driver_path} is executable")
                
            except Exception as e:
                logger.error(f"Failed to install ChromeDriver: {e}")
                return
        except ImportError:
            logger.warning("webdriver_manager is not installed")
        
        # Try to start Chrome with Selenium
        logger.info("Attempting to start Chrome with Selenium...")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        
        # Find Chrome binary
        chrome_binary = find_chrome_binary()
        if chrome_binary:
            options.binary_location = chrome_binary
        
        try:
            # Try with webdriver_manager if available
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            driver_path = ChromeDriverManager(path=test_dir).install()
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            
            logger.info("Successfully started Chrome with webdriver_manager")
            driver.quit()
            
        except Exception as e:
            logger.error(f"Failed to start Chrome with webdriver_manager: {e}")
            
            # Try with default Service
            try:
                from selenium.webdriver.chrome.service import Service
                service = Service()
                driver = webdriver.Chrome(service=service, options=options)
                
                logger.info("Successfully started Chrome with default Service")
                driver.quit()
                
            except Exception as e:
                logger.error(f"Failed to start Chrome with default Service: {e}")
                return
    
    except ImportError:
        logger.error("Selenium is not installed")

def main():
    """Main function"""
    logger.info("=== ChromeDriver Compatibility Check ===")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Python version: {sys.version}")
    
    # Check for Chrome/Chromium
    chrome_version = get_chrome_version()
    if chrome_version:
        logger.info(f"Chrome/Chromium version: {chrome_version}")
    else:
        logger.warning("Could not detect Chrome/Chromium version")
    
    # Find Chrome/Chromium binary
    chrome_binary = find_chrome_binary()
    
    # Check Selenium setup
    test_selenium_setup()
    
    logger.info("=== Check Complete ===")
    
    # Provide advice based on results
    if not chrome_version or not chrome_binary:
        print("\n== Action Required ==")
        print("Chrome/Chromium is not installed or not detected.")
        print("Please install Chrome or Chromium browser.")
        print("For Ubuntu/Debian: sudo apt install chromium-browser")
        print("For Fedora: sudo dnf install chromium")
        print("For Arch: sudo pacman -S chromium")
    else:
        print("\n== ChromeDriver Setup Advice ==")
        print(f"Your Chrome/Chromium version is {chrome_version}")
        print("Make sure your ChromeDriver version is compatible.")
        print("If you're having issues, try:")
        print("1. Install webdriver_manager: pip install webdriver_manager")
        print("2. Make sure the ChromeDriver executable has the right permissions (chmod +x)")
        print("3. Try adding '--no-sandbox' option to Chrome when running headless")

if __name__ == "__main__":
    main()

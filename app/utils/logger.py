import logging
from pathlib import Path
from datetime import datetime

from app.utils.config import get_log_file_path

def setup_logger():
    """Set up and configure the logger"""
    log_file = get_log_file_path()
    
    # Create a logger
    logger = logging.getLogger("linkedin_automation")
    logger.setLevel(logging.INFO)
    
    # Create handlers
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()
    
    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger, log_file

# Initialize logger
logger, log_file = setup_logger()

def log_content(content, content_type="generic"):
    """Log content to the log file with appropriate formatting"""
    logger.info(f"--- {content_type.upper()} CONTENT START ---")
    logger.info(content)
    logger.info(f"--- {content_type.upper()} CONTENT END ---")
    
    # Also write directly to the log file for better formatting of large content
    with open(log_file, 'a') as f:
        f.write(f"\n\n--- {content_type.upper()} CONTENT START ---\n")
        f.write(content)
        f.write(f"\n--- {content_type.upper()} CONTENT END ---\n\n")

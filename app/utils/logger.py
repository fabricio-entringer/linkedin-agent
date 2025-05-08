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
    
    # Clear any existing handlers to avoid duplication
    if logger.handlers:
        logger.handlers.clear()
    
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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log to the standard logger (this will go to both console and log file)
    logger.info(f"--- {content_type.upper()} CONTENT START at {timestamp} ---")
    logger.info(content)
    logger.info(f"--- {content_type.upper()} CONTENT END ---")
        
    # For message analysis, save to a dedicated file for easier reference
    if content_type == "linkedin_message_analysis":
        analysis_file = Path(log_file).parent / "message_analysis" / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        # Ensure the directory exists
        analysis_file.parent.mkdir(exist_ok=True)
        # Save the content
        with open(analysis_file, 'w') as f:
            f.write(f"LinkedIn Message Analysis - {timestamp}\n\n")
            f.write(content)
            f.write("\n\nEnd of Analysis")

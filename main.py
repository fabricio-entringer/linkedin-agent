#!/usr/bin/env python3
# 
# Note for GitHub Copilot: This project follows specific conventions.
# See .github/copilot-instructions.md for branch naming and PR formats.

import os
import sys
import time
import argparse

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.logger import logger
from app.utils.config import OPENAI_API_KEY
from app.agents.linkedin_agent import LinkedInMessageCrew

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="LinkedIn Message Analysis Tool")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with verbose logging")
    return parser.parse_args()

def main():
    """Main function to run the LinkedIn message analysis"""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Set debug environment variable if the debug flag is set
    if args.debug:
        os.environ["DEBUG"] = "true"
        logger.info("Debug mode enabled - verbose logging activated")
    
    # Check if all variable from .env file are set, for each one of them, log a warning if not, log the error and exit
    required_env_vars = ["OPENAI_API_KEY", "LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"]
    for var in required_env_vars:
        if not os.getenv(var):
            logger.error(f"Environment variable {var} is not set.")
            sys.exit(1)

    logger.info("Starting LinkedIn message analysis...")

    try:
        # Create and run the LinkedIn message crew
        crew = LinkedInMessageCrew().crew()
        
        # Run the crew
        result = crew.kickoff()
        
        logger.info("\033[92mLinkedIn message analysis completed successfully.\033[0m")
        
        return result
    
    except KeyboardInterrupt:
        logger.info("LinkedIn message analysis interrupted by user.")
    except Exception as e:
        logger.error(f"Error during LinkedIn message analysis: {e}")
    
    return None

if __name__ == "__main__":
    main()

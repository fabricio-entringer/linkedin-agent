#!/usr/bin/env python3

import os
import sys
import time
from crewai import Crew, Process

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.logger import logger
from app.utils.config import OPENAI_API_KEY
from app.agents.linkedin_agent import LinkedInMessageAgent

def main():
    """Main function to run the LinkedIn message analysis"""
    
    # Check if all variable from .env file are set, for each one of them, log a warning if not, log the error and exit
    required_env_vars = ["OPENAI_API_KEY", "LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"]
    for var in required_env_vars:
        if not os.getenv(var):
            logger.error(f"Environment variable {var} is not set.")
            sys.exit(1)

    logger.info("Starting LinkedIn message analysis...")

    try:
        # Create the LinkedIn message agent
        linkedin_agent = LinkedInMessageAgent()
        
        # Create the message analysis task
        message_task = linkedin_agent.create_message_task()
        
        # Create a crew with the LinkedIn agent
        crew = Crew(
            agents=[linkedin_agent.agent],
            tasks=[message_task],
            verbose=True,
            process=Process.sequential
        )
        
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

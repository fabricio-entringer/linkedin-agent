#!/usr/bin/env python3

import os
import sys
import time
from crewai import Crew, Process

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.logger import logger
from app.utils.config import OPENAI_API_KEY
from app.agents.linkedin_agent import LinkedInBrowserAgent

def main():
    """Main function to run the LinkedIn automation"""
    # Check if OpenAI API key is set
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)
    
    logger.info("Starting LinkedIn automation...")
    
    try:
        # Create the LinkedIn browser agent
        linkedin_agent = LinkedInBrowserAgent()
        
        # Create the browse task
        browse_task = linkedin_agent.create_browse_task()
        
        # Create a crew with the LinkedIn agent
        crew = Crew(
            agents=[linkedin_agent.agent],
            tasks=[browse_task],
            verbose=True,
            process=Process.sequential
        )
        
        # Run the crew
        result = crew.kickoff()
        
        logger.info("LinkedIn automation completed successfully.")
        logger.info(f"Result: {result}")
        
        return result
    
    except KeyboardInterrupt:
        logger.info("LinkedIn automation interrupted by user.")
    except Exception as e:
        logger.error(f"Error during LinkedIn automation: {e}")
    
    return None

if __name__ == "__main__":
    main()

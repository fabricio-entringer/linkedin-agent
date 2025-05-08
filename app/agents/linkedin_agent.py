from crewai import Agent, Task
from app.utils.logger import logger
from app.tools.linkedin import LinkedInTool

class LinkedInBrowserAgent:
    """An agent that browses LinkedIn and extracts content"""
    
    def __init__(self):
        self.linkedin_tool = LinkedInTool()
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create a CrewAI agent to browse LinkedIn"""
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4o-mini")
        
        return Agent(
            role="LinkedIn Browser",
            goal="Browse LinkedIn and extract content from the feed",
            backstory="I am an automated agent designed to browse LinkedIn, login to an account, "
                    "navigate to the feed, and extract the content for analysis.",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    def create_browse_task(self):
        """Create a task to browse LinkedIn"""
        from langchain.tools import tool
        
        @tool
        def browse_linkedin():
            """Browse LinkedIn and extract content from the feed"""
            return self._browse_linkedin()
        
        return Task(
            description="Browse LinkedIn and extract content from the feed. Extract the latest posts and updates from the LinkedIn feed to analyze trends and user engagement.",
            agent=self.agent,
            expected_output="A detailed summary of the content found on the LinkedIn feed",
            async_execution=False,
            tools=[browse_linkedin]
        )
    
    def _browse_linkedin(self) -> str:
        """Browse LinkedIn and extract content from the feed"""
        try:
            logger.info("Starting LinkedIn browsing task...")
            
            # Start the browser
            if not self.linkedin_tool.start():
                return "Failed to start the browser."
            
            # Login to LinkedIn
            if not self.linkedin_tool.login():
                self.linkedin_tool.close()
                logger.error("Login failed. Stopping the LinkedIn automation process.")
                return "Failed to login to LinkedIn. The application has been stopped to prevent multiple login attempts."
            
            # Go to the feed
            if not self.linkedin_tool.go_to_feed():
                self.linkedin_tool.close()
                return "Failed to navigate to the LinkedIn feed."
            
            # Extract content from the feed
            feed_content = self.linkedin_tool.extract_feed_content()
            
            # Close the browser
            self.linkedin_tool.close()
            
            return feed_content
        except Exception as e:
            logger.error(f"Error during LinkedIn browsing: {e}")
            try:
                self.linkedin_tool.close()
            except:
                pass
            return f"Error during LinkedIn browsing: {str(e)}"

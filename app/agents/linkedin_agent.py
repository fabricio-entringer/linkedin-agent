from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from app.utils.logger import logger, log_content
from app.tools.linkedin_tools import analyze_linkedin_messages
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class LinkedInMessageCrew:
    """A CrewAI crew that analyzes LinkedIn messages and suggests responses"""
    
    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        pass
    
    @agent
    def linkedin_analyst(self) -> Agent:
        """Create a CrewAI agent to analyze LinkedIn messages"""
        return Agent(
            config=self.agents_config['linkedin_analyst'],  # Use the config from agents.yaml
            verbose=True,
            allow_delegation=False,
            tools=[analyze_linkedin_messages]
        )
    
    @task
    def message_analysis_task(self) -> Task:
        """Create a task to analyze LinkedIn messages"""
        return Task(
            config=self.tasks_config['message_analysis_task'],  # Use the config from tasks.yaml
            tools=[analyze_linkedin_messages]
        )
    
    @crew
    def crew(self) -> Crew:
        """Create the LinkedIn message analysis crew"""
        return Crew(
            agents=self.agents,  # Automatically created by @agent decorator
            tasks=self.tasks,    # Automatically created by @task decorator
            verbose=True,
            process=Process.sequential
        )
    


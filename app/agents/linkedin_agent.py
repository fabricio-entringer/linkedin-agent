from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from app.utils.logger import logger, log_content
from app.tools.linkedin_tools import analyze_linkedin_messages
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
import os
import yaml

@CrewBase
class LinkedInMessageCrew:
    """A CrewAI crew that analyzes LinkedIn messages and suggests responses"""
    
    agents: List[BaseAgent]
    tasks: List[Task]
    agents_config: Dict[str, Any]
    tasks_config: Dict[str, Any]
    
    def __init__(self):
        # Initialize the configurations
        self.agents_config = self._load_config("agents.yaml")
        self.tasks_config = self._load_config("tasks.yaml")
    
    def _load_config(self, filename: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_path = os.path.join(os.path.dirname(__file__), "config", filename)
        try:
            with open(config_path, "r") as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}. Proceeding with empty configurations.")
            return {}
    
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
    


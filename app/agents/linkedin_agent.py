from crewai import Agent, Task
from crewai.tools import tool
from app.utils.logger import logger, log_content
from app.tools.linkedin import LinkedInTool

class LinkedInMessageAgent:
    """An agent that analyzes LinkedIn messages and suggests responses"""
    
    def __init__(self):
        self.linkedin_tool = LinkedInTool()
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create a CrewAI agent to analyze LinkedIn messages"""
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        
        return Agent(
            role="LinkedIn Message Analyst",
            goal="Analyze LinkedIn messages and suggest appropriate responses",
            backstory="I am an automated agent designed to access LinkedIn messages, login to an account, "
                    "analyze conversations, and suggest thoughtful responses based on the message context.",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    def create_message_task(self):
        """Create a task to analyze LinkedIn messages"""
        
        @tool
        def analyze_linkedin_messages():
            """Analyze LinkedIn messages and suggest responses"""
            return self._analyze_messages()
        
        return Task(
            description="Access LinkedIn messages, extract the latest conversations, and suggest appropriate responses for each message based on context and professional etiquette.",
            agent=self.agent,
            expected_output="A detailed analysis of recent LinkedIn messages with suggested responses",
            tools=[analyze_linkedin_messages]
        )
    
    def _analyze_messages(self) -> str:
        """Analyze LinkedIn messages and suggest responses"""
        try:
            logger.info("Starting LinkedIn message analysis task...")
            
            # Start the browser
            if not self.linkedin_tool.start():
                return "Failed to start the browser."
            
            # Login to LinkedIn
            if not self.linkedin_tool.login():
                self.linkedin_tool.close()
                logger.error("Login failed. Stopping the LinkedIn automation process.")
                return "Failed to login to LinkedIn. The application has been stopped to prevent multiple login attempts."
            
            # Go to the messages page
            if not self.linkedin_tool.go_to_messages():
                self.linkedin_tool.close()
                return "Failed to navigate to the LinkedIn messages."
            
            # Extract messages (latest 5)
            messages = self.linkedin_tool.extract_messages(limit=5)
            
            # Close the browser
            self.linkedin_tool.close()
            
            # If no messages were found
            if not messages:
                return "No messages found in LinkedIn chats."
            
            # Generate response suggestions for each message
            analyzed_messages = []
            
            for msg in messages:
                contact = msg['contact']
                message = msg['message']
                
                # Generate a potential response using the LLM
                suggestion = self._generate_response_suggestion(contact, message)
                
                analyzed_messages.append({
                    "contact": contact,
                    "message": message,
                    "potential_answer": suggestion
                })
            
            # Format the output for display and logging
            output = "\n\n".join([
                f"Contact: {msg['contact']}\n"
                f"Message: {msg['message']}\n"
                f"Potential Answer: {msg['potential_answer']}\n"
                f"{'=' * 50}"
                for msg in analyzed_messages
            ])
            
            # Log the analyzed messages
            log_content(output, "linkedin_message_analysis")
            
            return output
        except Exception as e:
            logger.error(f"Error during LinkedIn message analysis: {e}")
            try:
                self.linkedin_tool.close()
            except:
                pass
            return f"Error during LinkedIn message analysis: {str(e)}"
            
    def _generate_response_suggestion(self, contact, message):
        """Generate a response suggestion for a given message"""
        try:
            # Use the LLM to generate a response
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage, SystemMessage
            
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
            
            # Determine the message type to customize the response
            message_type = self._determine_message_type(message)
            
            # Construct the prompt based on message type
            system_prompt = (
                "You are a professional LinkedIn communication assistant. "
                "Generate a thoughtful, concise, and professional response to the following LinkedIn message. "
            )
            
            if message_type == "connection_request":
                system_prompt += (
                    "This appears to be a connection request or introduction. "
                    "Be appreciative and show interest in connecting. "
                    "Keep the response friendly, professional, and under 80 words."
                )
            elif message_type == "job_opportunity":
                system_prompt += (
                    "This appears to be related to a job opportunity. "
                    "Express appropriate interest or gratitude while maintaining professionalism. "
                    "Ask 1-2 relevant follow-up questions if appropriate. "
                    "Keep the response under 100 words."
                )
            elif message_type == "sales_pitch":
                system_prompt += (
                    "This appears to be a sales pitch or service offering. "
                    "Be polite but direct about your level of interest. "
                    "If declining, be respectful. If interested, ask a specific question. "
                    "Keep the response under 80 words."
                )
            else:
                system_prompt += (
                    "Respond in a friendly but professional manner. "
                    "Match the tone and formality of the original message. "
                    "Keep the response under 100 words."
                )
            
            user_prompt = f"Contact: {contact}\nMessage: {message}\n\nSuggested response:"
            
            response = llm([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            return response.content.strip()
        except Exception as e:
            logger.error(f"Failed to generate response suggestion: {e}")
            return "Could not generate a suggestion due to an error."
            
    def _determine_message_type(self, message):
        """Determine the type of LinkedIn message to tailor the response"""
        message = message.lower()
        
        # Connection request or introduction
        if any(term in message for term in ['connect', 'connection', 'network', 'nice to meet', 'introduction']):
            return "connection_request"
            
        # Job opportunity
        if any(term in message for term in ['job', 'position', 'opportunity', 'hiring', 'recruit', 'opening', 'role']):
            return "job_opportunity"
            
        # Sales pitch
        if any(term in message for term in ['offer', 'service', 'product', 'solution', 'discount', 'demo', 'free trial']):
            return "sales_pitch"
            
        # Default - general conversation
        return "general"

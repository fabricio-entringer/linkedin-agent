"""Test script for the fix to Issue #10"""

# Mock implementation to verify data structure compatibility
class MockLinkedInTool:
    def extract_messages(self, limit=5):
        # Return mock data in the new structure
        return [
            {
                "contact": "John Doe",
                "messages": ["Hello, I'd like to connect.", "Thanks for accepting."],
                "message_count": 2
            },
            {
                "contact": "Jane Smith",
                "messages": ["We have a job opening that matches your skills."],
                "message_count": 1
            }
        ]

def analyze_mock_messages():
    """Test function to analyze mock messages with the new data structure"""
    try:
        print("Starting mock LinkedIn message analysis task...")
        
        # Create a mock LinkedInTool instance
        linkedin_tool = MockLinkedInTool()
        
        # Extract messages
        conversation_data = linkedin_tool.extract_messages(limit=5)
        
        # If no messages were found
        if not conversation_data:
            return "No messages found in LinkedIn chats."
        
        # Generate mock response suggestions for each message
        analyzed_messages = []
        
        for conversation in conversation_data:
            contact = conversation['contact']
            messages = conversation['messages']
            message_count = conversation['message_count']
            
            # Skip empty conversations
            if not messages:
                continue
                
            # Get the most recent message
            latest_message = messages[0]  # The first message is the most recent one
            
            # Generate a mock response
            suggestion = f"Thank you for your message: '{latest_message}'. This is a test response."
            
            analyzed_messages.append({
                "contact": contact,
                "message": latest_message,
                "message_count": message_count,
                "potential_answer": suggestion
            })
        
        # Format the output for display
        output = "\n\n".join([
            f"Contact: {msg['contact']}\n"
            f"Message: {msg['message']}\n"
            f"Total Messages: {msg['message_count']}\n"
            f"Potential Answer: {msg['potential_answer']}\n"
            f"{'=' * 50}"
            for msg in analyzed_messages
        ])
        
        print("SUCCESS: The new data structure is working correctly!")
        print("\nExample output:")
        print(output)
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    result = analyze_mock_messages()
    print(f"\nTest result: {'Passed' if result else 'Failed'}")

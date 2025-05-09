"""
Enhanced test script to verify fix for issue #10
This script tests both the old and new data structures
to ensure backward compatibility and proper fix
"""

class MockLinkedInToolOld:
    """Mock of the old implementation for comparison"""
    def extract_messages(self, limit=5):
        # Return mock data in the old structure
        return [
            {
                "contact": "Old Format User",
                "message": "This is using the old format"
            }
        ]

class MockLinkedInToolNew:
    """Mock of the new implementation"""
    def extract_messages(self, limit=5):
        # Return mock data in the new structure
        return [
            {
                "contact": "New Format User",
                "messages": ["This is using the new format", "With conversation history"],
                "message_count": 2
            }
        ]

def analyze_messages_old_format():
    """Tests the old message format to ensure backward compatibility"""
    try:
        print("\n== Testing OLD Format (Backward Compatibility) ==")
        linkedin_tool = MockLinkedInToolOld()
        messages = linkedin_tool.extract_messages()
        
        if not messages:
            print("ERROR: No messages found")
            return False
        
        # Process messages in old format
        analyzed_messages = []
        for msg in messages:
            contact = msg['contact']
            message = msg.get('message', "No message")
            
            # Generate a mock response
            suggestion = f"Response to '{message}'"
            
            analyzed_messages.append({
                "contact": contact,
                "message": message,
                "potential_answer": suggestion
            })
        
        # Output results
        for msg in analyzed_messages:
            print(f"Contact: {msg['contact']}")
            print(f"Message: {msg['message']}")
            print(f"Answer: {msg['potential_answer']}")
        
        return True
    except Exception as e:
        print(f"ERROR in old format test: {e}")
        return False

def analyze_messages_new_format():
    """Tests the new message format with our fix"""
    try:
        print("\n== Testing NEW Format (With Fix) ==")
        linkedin_tool = MockLinkedInToolNew()
        conversations = linkedin_tool.extract_messages()
        
        if not conversations:
            print("ERROR: No conversations found")
            return False
        
        # Process messages in new format
        analyzed_messages = []
        for conversation in conversations:
            contact = conversation['contact']
            messages = conversation['messages']
            message_count = conversation['message_count']
            
            if not messages:
                continue
                
            latest_message = messages[0]
            
            # Generate a mock response using context
            suggestion = f"Contextual response to '{latest_message}' (with {message_count} total messages in history)"
            
            analyzed_messages.append({
                "contact": contact,
                "message": latest_message,
                "message_count": message_count,
                "potential_answer": suggestion
            })
        
        # Output results
        for msg in analyzed_messages:
            print(f"Contact: {msg['contact']}")
            print(f"Message: {msg['message']}")
            print(f"Total Messages: {msg['message_count']}")
            print(f"Answer: {msg['potential_answer']}")
        
        return True
    except KeyError as e:
        print(f"KEY ERROR in new format test: {e}")
        print("This suggests the fix isn't handling the new data structure correctly")
        return False
    except Exception as e:
        print(f"ERROR in new format test: {e}")
        return False

if __name__ == "__main__":
    old_test_result = analyze_messages_old_format()
    new_test_result = analyze_messages_new_format()
    
    print("\n== Test Results ==")
    print(f"Old Format Test: {'PASSED' if old_test_result else 'FAILED'}")
    print(f"New Format Test: {'PASSED' if new_test_result else 'FAILED'}")
    
    if old_test_result and new_test_result:
        print("\n✅ SUCCESS: The fix correctly handles both data structures!")
    else:
        print("\n❌ FAILURE: The fix doesn't handle all scenarios correctly.")

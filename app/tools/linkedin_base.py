from bs4 import BeautifulSoup
from datetime import datetime
from app.utils.logger import logger, log_content

class LinkedInChatExtractor:
    """A tool for extracting LinkedIn chat conversations from HTML"""
    
    def extract_chat_from_html(self, html_content):
        """Extract a complete LinkedIn chat conversation from HTML
        
        Args:
            html_content (str): HTML content of the LinkedIn chat page
            
        Returns:
            dict: Structured conversation data containing all messages and metadata
        """
        logger.info("Extracting LinkedIn chat conversation from HTML")
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract conversation metadata
            conversation_data = {
                "participants": self._extract_participants(soup),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "messages": self._extract_messages(soup)
            }
            
            # Format content for logging
            formatted_content = self._format_conversation(conversation_data)
            
            # Log the extracted content
            log_content(formatted_content, "linkedin_chat")
            
            logger.info(f"Successfully extracted LinkedIn chat with {len(conversation_data['messages'])} messages")
            return conversation_data
            
        except Exception as e:
            logger.error(f"Error extracting chat conversation: {e}")
            return None
    
    def _extract_participants(self, soup):
        """Extract participants from the chat"""
        participants = []
        
        # Extract the primary participant (the one you're chatting with)
        title_element = soup.find("h2", {"class": "msg-entity-lockup__entity-title"})
        if title_element:
            primary_participant = title_element.text.strip()
            participants.append({
                "name": primary_participant,
                "is_premium": bool(soup.find("svg", {"data-test-icon": "linkedin-bug-premium-v2-xxsmall"})),
                "status": "Available" if soup.find("div", {"class": "presence-indicator--is-reachable"}) else "Offline",
                "profile_link": soup.find("a", {"title": lambda x: x and "profile" in x.lower()})["href"] if soup.find("a", {"title": lambda x: x and "profile" in x.lower()}) else None
            })
        
        # Extract the current user (yourself)
        # This is trickier as it's not always clearly labeled in the HTML
        # We'll look for messages sent by you
        your_message = soup.find("div", {"class": "msg-s-event-listitem", "data-event-urn": lambda x: x and not "msg-s-event-listitem--other" in " ".join(soup.find("div", {"data-event-urn": x})["class"])})
        if your_message:
            your_link = your_message.find("a", {"class": "msg-s-event-listitem__link"})
            if your_link:
                profile_img = your_link.find("img")
                if profile_img and profile_img.get("title"):
                    participants.append({
                        "name": profile_img["title"],
                        "is_premium": False,  # This could be updated if needed
                        "status": "Online",  # Assuming you're online
                        "profile_link": your_link["href"]
                    })
        
        return participants
    
    def _extract_messages(self, soup):
        """Extract all messages from the conversation"""
        messages = []
        
        # Find all message events
        message_events = soup.find_all("li", {"class": "msg-s-message-list__event"})
        
        for event in message_events:
            # Skip time headers
            if event.find("time", {"class": "msg-s-message-list__time-heading"}):
                continue
                
            # Extract message data
            message = self._parse_message_event(event)
            if message:
                messages.append(message)
        
        return messages
    
    def _parse_message_event(self, event):
        """Parse a single message event"""
        try:
            # Get message container
            msg_container = event.find("div", {"class": "msg-s-event-listitem"})
            if not msg_container:
                return None
                
            # Determine sender
            is_other = "msg-s-event-listitem--other" in msg_container.get("class", [])
            
            # Get sender information
            sender_img = msg_container.find("img", {"class": "msg-s-event-listitem__profile-picture"})
            sender_name = sender_img.get("title", "Unknown") if sender_img else "Unknown"
            
            # Get metadata
            meta_div = msg_container.find("div", {"class": "msg-s-message-group__meta"})
            timestamp = meta_div.find("time").text.strip() if meta_div and meta_div.find("time") else "Unknown time"
            
            # Get message content
            content_p = msg_container.find("p", {"class": "msg-s-event-listitem__body"})
            content = content_p.get_text(separator="\n").strip() if content_p else ""
            
            # Check for reactions
            reactions = []
            reactions_container = msg_container.find("ul", {"class": "msg-reactions-reaction-summary-presenter__container"})
            if reactions_container:
                reaction_pills = reactions_container.find_all("li", {"class": "msg-reactions-reaction-summary-presenter__pill-container"})
                for pill in reaction_pills:
                    emoji_element = pill.find("span", {"class": "msg-reactions-reaction-summary-presenter__pill-emoji"})
                    count_element = pill.find("span", {"class": "emoji-count"})
                    if emoji_element and count_element:
                        reactions.append({
                            "emoji": emoji_element.text.strip(),
                            "count": int(count_element.text.strip())
                        })
            
            # Check for link previews
            link_previews = []
            link_preview_div = msg_container.find("div", {"class": "msg-s-event-listitem__unrolled-update-v2"})
            if link_preview_div:
                link_element = link_preview_div.find("a", {"class": "tap-target"})
                if link_element:
                    link_previews.append({
                        "url": link_element["href"],
                        "title": link_element.get("aria-label", "").replace("Open article: ", "") if link_element.get("aria-label") else "Link preview"
                    })
            
            # Check if message was sent successfully
            sending_indicator = msg_container.find("span", {"class": "msg-s-event-with-indicator__sending-indicator"})
            sent_status = "sent" if sending_indicator and "msg-s-event-with-indicator__sending-indicator--sent" in sending_indicator["class"] else "unknown"
            
            return {
                "sender": sender_name,
                "is_other": is_other,
                "timestamp": timestamp,
                "content": content,
                "reactions": reactions,
                "link_previews": link_previews,
                "status": sent_status
            }
            
        except Exception as e:
            logger.error(f"Error parsing message event: {e}")
            return None
    
    def _format_conversation(self, conversation_data):
        """Format the conversation data for logging"""
        formatted = f"LinkedIn Chat Conversation\n"
        formatted += f"===========================\n\n"
        
        # Participants
        formatted += f"Participants:\n"
        for participant in conversation_data["participants"]:
            premium_status = "Premium" if participant["is_premium"] else "Standard"
            formatted += f"- {participant['name']} ({premium_status}, {participant['status']})\n"
        
        formatted += f"\nDate: {conversation_data['date']}\n"
        formatted += f"Messages: {len(conversation_data['messages'])}\n\n"
        formatted += f"===========================\n\n"
        
        # Messages
        for msg in conversation_data["messages"]:
            sender_prefix = "→" if msg["is_other"] else "←"
            formatted += f"{sender_prefix} {msg['sender']} ({msg['timestamp']}):\n"
            formatted += f"{msg['content']}\n"
            
            # Add reactions if any
            if msg["reactions"]:
                reactions_str = ", ".join([f"{r['emoji']} ({r['count']})" for r in msg["reactions"]])
                formatted += f"Reactions: {reactions_str}\n"
                
            # Add link previews if any
            if msg["link_previews"]:
                for preview in msg["link_previews"]:
                    formatted += f"Link: {preview['url']} - {preview['title']}\n"
                    
            formatted += f"\n"
        
        return formatted

def extract_linkedin_chat(html_file_path):
    """Helper function to extract LinkedIn chat from an HTML file"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        extractor = LinkedInChatExtractor()
        return extractor.extract_chat_from_html(html_content)
    except Exception as e:
        logger.error(f"Error reading HTML file {html_file_path}: {e}")
        return None

if __name__ == "__main__":
    # This can be used to test the extraction from command line
    import sys
    if len(sys.argv) > 1:
        result = extract_linkedin_chat(sys.argv[1])
        print(f"Extracted {len(result['messages'])} messages")
    else:
        print("Please provide the path to an HTML file")
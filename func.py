import os
from waveshare_epd import epd4in2_V2
#from PIL import Image,ImageDraw,ImageFont
import json
from datetime import datetime
import uuid
from PIL import Image,ImageDraw,ImageFont

def font(size):
    return ImageFont.truetype(os.path.join("./pic", 'Font.ttc'), size)

def clear_screen():
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()

def sleep():
    epd = epd4in2_V2.EPD()

    epd.init()
    epd.Clear()
    epd.sleep()
    epd4in2_V2.epdconfig.module_exit(cleanup=True)
    print("Done!")
    exit()


### Message saving stuff ###

# Convert Python object to JSON string
def to_json_string(data):
    return json.dumps(data, indent=2)

# Convert JSON string to Python object
def from_json_string(json_string):
    return json.loads(json_string)

# Write Python object to JSON file
def write_json_file(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# Read JSON file to Python object
def read_json_file(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        return json.load(f)


class MessageStore:
    def __init__(self, storage_dir="data"):
        self.storage_dir = storage_dir
        self.conversations_file = os.path.join(storage_dir, "conversations.json")
        
        # Create storage directory if it doesn't exist
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        
        # Initialize conversations file if it doesn't exist
        if not os.path.exists(self.conversations_file):
            self._initialize_conversations_file()
    
    def _initialize_conversations_file(self):
        """Create an empty conversations file"""
        initial_data = {"conversations": {}}
        write_json_file(initial_data, self.conversations_file)
    
    def get_all_conversations(self):
        """Get all conversations"""
        data = read_json_file(self.conversations_file)
        if data is None:
            return {}
        return data.get("conversations", {})
    
    def get_conversation(self, phone_number):
        """Get a specific conversation by phone number"""
        conversations = self.get_all_conversations()
        return conversations.get(phone_number, {
            "contact_name": phone_number,
            "last_active": None,
            "unread_count": 0,
            "messages": []
        })
    
    def save_message(self, phone_number, message_content, is_incoming=True, status="unread"):
        """Save a new message to a conversation"""
        # Load existing data
        data = read_json_file(self.conversations_file)
        if data is None:
            self._initialize_conversations_file()
            data = {"conversations": {}}
        
        # Get or create conversation
        if phone_number not in data["conversations"]:
            data["conversations"][phone_number] = {
                "contact_name": phone_number,  # Could be updated with contact name later
                "last_active": datetime.now().isoformat(),
                "unread_count": 1 if is_incoming else 0,
                "messages": []
            }
        else:
            # Update conversation metadata
            data["conversations"][phone_number]["last_active"] = datetime.now().isoformat()
            if is_incoming and status == "unread":
                data["conversations"][phone_number]["unread_count"] += 1
        
        # Create new message
        message = {
            "id": f"msg_{uuid.uuid4().hex[:8]}",
            "content": message_content,
            "timestamp": datetime.now().isoformat(),
            "is_incoming": is_incoming,
            "status": status
        }
        
        # Add message to conversation
        data["conversations"][phone_number]["messages"].append(message)
        
        # Save updated data
        write_json_file(data, self.conversations_file)
        
        return message
    
    def mark_as_read(self, phone_number, message_id=None):
        """Mark message(s) as read"""
        data = read_json_file(self.conversations_file)
        if data is None or phone_number not in data["conversations"]:
            return False
        
        conversation = data["conversations"][phone_number]
        
        if message_id:
            # Mark specific message as read
            for message in conversation["messages"]:
                if message["id"] == message_id and message["status"] == "unread":
                    message["status"] = "read"
                    conversation["unread_count"] = max(0, conversation["unread_count"] - 1)
        else:
            # Mark all messages in conversation as read
            for message in conversation["messages"]:
                if message["status"] == "unread":
                    message["status"] = "read"
            conversation["unread_count"] = 0
        
        write_json_file(data, self.conversations_file)
        return True

import os
from waveshare_epd import epd4in2_V2
#from PIL import Image,ImageDraw,ImageFont
import json
from datetime import datetime
import uuid
from PIL import Image,ImageDraw,ImageFont

### Screen tools ###

def calculate_size(draw, text, font):
    bbox = draw.textbbox((0,0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return (text_width, text_height)

def font(size):
    return ImageFont.truetype(os.path.join("./pic", 'Font.ttc'), size) # Builit in font
    # return ImageFont.truetype(os.path.join("./pic", 'Roboto-Regular.ttf'), size) # Font I added

def clear_screen():
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()
    #clear_draw(draw)

def clear_draw(draw):
    draw.rectangle([(0, 0), (1000, 1000)], fill="white")

def sleep():
    epd = epd4in2_V2.EPD()

    epd.init()
    epd.Clear()
    epd.sleep()
    epd4in2_V2.epdconfig.module_exit(cleanup=True)
    print("Done!")
    exit()

def draw_with_wrap(draw, location, text, wrap_width, font, alignment='left', no_draw = False): # We are only using the y value in location for now, it just makes more sense for rn
    words = text.split()
    running_width = 0
    adding_y = location[1]
    line_draw = []
    left_align_x_value = 10
    right_align_x_value = 290
    for word in words:
        width, height = calculate_size(draw, word, font=font)
        running_width += width
        if running_width < wrap_width:
            line_draw.append(word)
        else:
            if alignment == 'left':
                x_position = left_align_x_value
            else:
                x_position = right_align_x_value - calculate_size(draw, ' '.join(line_draw), font=font)[0]
            if no_draw == False:
                draw.text((x_position, adding_y), ' '.join(line_draw), font=font, fill=0)
            adding_y += calculate_size(draw, ' '.join(line_draw), font=font)[1] + 5  # Add space between lines
            line_draw = [word]  # Start new line with the current word
            running_width = width  # Reset running width to the current word's width
    # Draw any remaining words in the last line
    if alignment == 'left':
                x_position = left_align_x_value
    else:
        x_position = right_align_x_value - calculate_size(draw, ' '.join(line_draw), font=font)[0]
    if line_draw:
        if no_draw == False:
            draw.text((x_position, adding_y), ' '.join(line_draw), font=font, fill=0)
    if adding_y == location[1]:
        adding_y = adding_y + calculate_size(draw, ' '.join(line_draw), font=font)[1]
    # print(f"{adding_y}, {location[1]}")
    return adding_y - location[1]
    


######################################

def convert_time(input, version='hr-min'):
    if version == 'hr-min':
        dt_object = datetime.fromisoformat(input)
        hour_minute = dt_object.strftime("%H:%M")
        return hour_minute


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
            "last_message_time": None,
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
                "last_message_time": datetime.now().isoformat(),
                "unread_count": 1 if is_incoming else 0,
                "messages": []
            }
        else:
            # Update conversation metadata
            data["conversations"][phone_number]["last_message_time"] = datetime.now().isoformat()
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

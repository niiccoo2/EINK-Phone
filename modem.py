#!/usr/bin/env python

"""
Demo: Send Simple SMS Demo

Simple demo to send sms via gsmmodem package
"""

from gsmmodem.modem import GsmModem, SentSms, CmsError  # type: ignore
import sys
import os
libdir = "./waveshare_epd"
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
import random
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd4in2_V2 # type: ignore
from func import *

epd = epd4in2_V2.EPD()

# We can check using the 'mode' command in cmd
PORT = '/dev/ttyUSB2'
BAUDRATE = 115200
SMS_TEXT = "Text from E-INK Phone, number " + str(random.randint(1000, 9999))
SMS_DESTINATION = '6172060139'
PIN = None  # SIM card PIN (if any)
store = MessageStore()
modem_init = False

ScreenImage1 = Image.new('1', (epd.height, epd.width), 255)  # 255: Set all pixels to white 

draw = ImageDraw.Draw(ScreenImage1)

modem = None  # Global variable to hold the modem instance

def nothing():
    pass

state = {
    'screen': nothing,
    'page': 0,
    'index': 0,
    'number': '+10000000000'
}

original_handle_status_report = GsmModem._handleSmsStatusReport

# Define a patched version
def patched_handle_status_report(self, line):
    try:
        original_handle_status_report(self, line)
    except CmsError as e:
        if e.code == 321:
            print("Ignored CMS ERROR 321 (no delivery report found)")
        else:
            raise  # Reraise other errors

# Patch the method
GsmModem._handleSmsStatusReport = patched_handle_status_report

def extract_conversation_details(filepath):
    data = read_json_file(filepath)
    if not data or "conversations" not in data:
        return {}

    conversation_details = {}
    for number, details in data["conversations"].items():
        last_message = details["messages"][-1]["content"] if details["messages"] else "No messages"
        conversation_details[number] = {
            "name": details.get("contact_name", "Unknown"),
            "last_message_time": details.get("last_message_time", "Unknown"),
            "last_message": last_message,
            "Location": (0, 0)
        }
    
    return conversation_details

def load_conversation_data(phone_number):
    # Load the conversation data from the JSON file
    data = read_json_file("data/conversations.json")
    
    # Check if the data is valid and contains conversations
    if not data or "conversations" not in data:
        return {}
    
    # Initialize a dictionary to hold the conversation details
    conversation = {}
    # print(data["conversations"])
    # Check if the phone number exists in the conversations
    if phone_number in data["conversations"]:
        details = data["conversations"][phone_number]
        conversation["contact_name"] = details.get("contact_name", "Unknown")
        conversation["messages"] = details.get("messages", [])
        conversation["last_message_time"] = details.get("last_message_time", "Unknown")
    else:
        print(f"No conversation found for {phone_number}")
    
    return conversation

conversation_details = extract_conversation_details("data/conversations.json")
conversation_keys = list(conversation_details.keys())

def process_incoming_sms(sms): # Function that runs whenever a sms is received
    print(f"Got text from {sms.number}: {sms.text}")
    store.save_message(sms.number, sms.text)
    if state['screen'] == open_conversation:
        state['screen'](state['number'])
    else:
        state['screen']()

def init_modem(): # Initalizes the modem
    global modem_init
    global modem  # Declare that we are using the global variable
    print('Initializing modem...')
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=process_incoming_sms)
    modem.connect(PIN)
    modem.waitForNetworkCoverage(10)
    modem.smsTextMode = True
    modem_init = True
    print('Modem initialized.\n')

def send_sms_message(number, text): # Send a text, not done yet
    print('Sending SMS to: {0}'.format(number))
    response = modem.sendSms(number, text, waitForDeliveryReport=False)
    if type(response) == SentSms:
        print('SMS Delivered.')
    else:
        print('SMS Could not be sent')

def draw_conversation(start_location, name, time, body, selected = False): # Draws the message neatly on the screen
    # Calculate positions based on the starting location
    name_width, name_height = calculate_size(draw, name, font(20))
    draw.text((10, start_location + 10), str(name), font=font(20), fill=0)
    draw.text((240, start_location + 10), str(time), font=font(20), fill=0)
    draw.text((10, start_location + 50), str(body), font=font(20), fill=0)
    draw.line([(0, start_location + 90), (300, start_location + 90)], fill=None, width=2, joint=None)
    if selected == True:
        draw.line([(10, start_location+17+name_height), (10+name_width, start_location+17+name_height)], fill=None, width=2, joint=None)
        #print(name_width, name_height)



def draw_messages_screen(selected_index, current_page):
    global conversation_details
    conversations_per_page = 4
    start_index = current_page * conversations_per_page
    end_index = min(start_index + conversations_per_page, len(conversation_keys))
    for index, number in enumerate(conversation_keys[start_index:end_index]):
        details = conversation_details[number]
        if index == selected_index:
            draw_conversation(index * 100, details['name'], convert_time(details['last_message_time']), details['last_message'], True)
        else:
            draw_conversation(index * 100, details['name'], convert_time(details['last_message_time']), details['last_message'])
    epd.display_Partial(epd.getbuffer(ScreenImage1))

def draw_message_view(number, current_page):
    clear_draw(draw)

    conversation = load_conversation_data(number)
    all_messages = conversation.get('messages', [])[::-1]  # Reverse the list to start with the most recent messages

    page_stop = 0
    adding_y = 400  # Start drawing from the bottom of the screen
    messages_per_page = []
    current_page_messages = []

    for message in all_messages:
        # Calculate the height of the message without drawing it
        height = draw_with_wrap(draw, (10, adding_y), message.get('content', 'N/A'), 200, font=font(15), alignment='left', no_draw=True)
        
        # Check if the message fits on the current page
        if adding_y - height < page_stop:
            # If it doesn't fit, store the current page's messages and start a new page
            messages_per_page.append(current_page_messages)
            current_page_messages = []
            adding_y = 380  # Reset y position for the new page

        # Add the message to the current page
        current_page_messages.append(message)
        adding_y -= height + 10

    # Add the last page's messages
    if current_page_messages:
        messages_per_page.append(current_page_messages)

    # Display the messages for the current page
    adding_y = 380  # Reset y position for drawing
    for message in messages_per_page[current_page]:
        if message.get('is_incoming', 'N/A') == True:
            draw_with_wrap(draw, (10, adding_y), message.get('content', 'N/A'), 200, font=font(15))
        elif message.get('is_incoming', 'N/A') == False:
            draw_with_wrap(draw, (10, adding_y), message.get('content', 'N/A'), 200, font=font(15), alignment='right')
        adding_y -= height + 10

    epd.display_Partial(epd.getbuffer(ScreenImage1))




def open_conversation(number):
    global state
    state['number'] = number
    state['screen'] = open_conversation
    page_number = 0
    draw_message_view(number, page_number)
    
    while True:
        user_input = input("Message: ")
        if user_input == 'exit':
            return
        elif user_input == 'w':
            page_number += 1
            if page_number < 0:
                page_number = 0
        elif user_input == 's':
            page_number -= 1
        else:
            send_sms_message(number, user_input)
            store.save_message(number, user_input, is_incoming=False)
        clear_draw(draw)
        draw_message_view(number, page_number)


def messages_app(): 
    global conversation_details
    global state
    state['screen'] = messages_app
    conversation_details = extract_conversation_details("data/conversations.json")
    conversation_keys = list(conversation_details.keys())
    # selected_index = 0
    # current_page = 0
    conversations_per_page = 4
    total_pages = (len(conversation_keys) + conversations_per_page - 1) // conversations_per_page

    clear_draw(draw)

    clear_screen()
    if modem_init == False:
        init_modem()

    draw_messages_screen(state['index'], state['page'])

    while True:
        user_input = input("Input: ")
        if user_input == "exit":
            return
        elif user_input == "s":
            state['index'] += 1
            if state['index'] + (state['page']) * conversations_per_page >= len(conversation_keys):
                state['index'] = (len(conversation_keys) % conversations_per_page) - 1
            if state['index'] >= conversations_per_page:
                state['index'] = 0
                state['page'] += 1
                if state['page'] >= total_pages:
                    state['page'] = total_pages - 1
        elif user_input == "w":
            state['index'] -= 1
            if state['index'] < 0:
                state['index'] = conversations_per_page - 1
                state['page'] -= 1
                if state['page'] < 0:
                    state['page'] = 0
                    state['index'] = 0
        
        ### Logic that skips pages ###
        # elif user_input == "n":  # Next page
        #     current_page += 1
        #     if current_page >= total_pages:
        #         current_page = total_pages - 1
        # elif user_input == "p":  # Previous page
        #     current_page -= 1
        #     if current_page < 0:
        #         current_page = 0
        ##################################

        elif user_input == "e":
            print("Running the selected app")
            open_conversation(conversation_keys[state['index'] + state['page'] * conversations_per_page])
            clear_screen()
        print(state['index'])
        print(state['page'])
        print(conversation_keys)
        clear_draw(draw)
        draw_messages_screen(state['index'], state['page'])


    #time.sleep(10)
    return
    # try:
    #     #modem.running = True
    #     while True:
    #         # Keep the program running to listen for SMS messages
    #         pass
    # except KeyboardInterrupt:
    #     print("Exiting...")
    #     #modem.close()
    #     return



if __name__ == "__main__":
    epd.init()
    epd.Clear()
    print(draw_with_wrap(draw, (10, 10), "This", 200, font(15), alignment='left'))
    print(draw_with_wrap(draw, (10, 40), "This should be a lot of lines that we need to test this thing.", 200, font(15), alignment='left'))
    draw.line([(10,50), (10, 62)], fill=None, width=2, joint=None)
    draw.line([(10,70), (10, 87)], fill=None, width=2, joint=None)
    epd.display_Partial(epd.getbuffer(ScreenImage1))
    epd.sleep()
    exit()

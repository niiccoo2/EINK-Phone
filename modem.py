#!/usr/bin/env python

"""
Demo: Send Simple SMS Demo

Simple demo to send sms via gsmmodem package
"""

from gsmmodem.modem import GsmModem, SentSms  # type: ignore
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

conversation_details = extract_conversation_details("data/conversations.json")
conversation_keys = list(conversation_details.keys())

def process_incoming_sms(sms): # Function that runs whenever a sms is received
    print(f"Got text from {sms.number}: {sms.text}")
    store.save_message(sms.number, sms.text)

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

def draw_message(start_location, name, time, body, selected = False): # Draws the message neatly on the screen
    # Calculate positions based on the starting location
    name_width, name_height = calculate_size(draw, name, font(20))
    draw.text((10, start_location + 10), str(name), font=font(20), fill=0)
    draw.text((240, start_location + 10), str(time), font=font(20), fill=0)
    draw.text((10, start_location + 50), str(body), font=font(20), fill=0)
    draw.line([(0, start_location + 90), (300, start_location + 90)], fill=None, width=2, joint=None)
    if selected == True:
        draw.line([(10, start_location+17+name_height), (10+name_width, start_location+17+name_height)], fill=None, width=2, joint=None)
        print(name_width, name_height)

# def draw_messages_screen(selected_index, adding_y=0):
#     global conversation_details
#     index = 0
#     for number, details in conversation_details.items():
#         if index == selected_index:
#             draw_message(adding_y, details['name'], convert_time(details['last_message_time']), details['last_message'], True)
#         else:
#             draw_message(adding_y, details['name'], convert_time(details['last_message_time']), details['last_message'])
#         adding_y = adding_y + 100
#         index = index + 1
#     epd.display_Partial(epd.getbuffer(ScreenImage1))

def draw_messages_screen(selected_index, current_page):
    global conversation_details
    conversations_per_page = 4
    start_index = current_page * conversations_per_page
    end_index = min(start_index + conversations_per_page, len(conversation_keys))
    for index, number in enumerate(conversation_keys[start_index:end_index]):
        details = conversation_details[number]
        if index == selected_index:
            draw_message(index * 100, details['name'], convert_time(details['last_message_time']), details['last_message'], True)
        else:
            draw_message(index * 100, details['name'], convert_time(details['last_message_time']), details['last_message'])
    epd.display_Partial(epd.getbuffer(ScreenImage1))

def open_conversation(number):
    pass

def messages_app(): 
    global conversation_details
    conversation_details = extract_conversation_details("data/conversations.json")
    conversation_keys = list(conversation_details.keys())
    selected_index = 0
    current_page = 0
    conversations_per_page = 4
    total_pages = (len(conversation_keys) + conversations_per_page - 1) // conversations_per_page

    clear_draw(draw)

    clear_screen()
    if modem_init == False:
        init_modem()

    draw_messages_screen(selected_index, current_page)

    while True:
        user_input = input("Input: ")
        if user_input == "exit":
            break
        elif user_input == "s":
            selected_index += 1
            if selected_index >= conversations_per_page:
                selected_index = 0
                current_page += 1
                if current_page >= total_pages:
                    current_page = total_pages - 1
        elif user_input == "w":
            selected_index -= 1
            if selected_index < 0:
                selected_index = conversations_per_page - 1
                current_page -= 1
                if current_page < 0:
                    current_page = 0
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
            open_conversation(conversation_keys[selected_index + current_page * conversations_per_page])
            clear_screen()
        
        clear_draw(draw)
        draw_messages_screen(selected_index, current_page)


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
    print("Done with the clear")
    # init_modem()
    # messages()
    # draw.rectangle([(0, 0), (1000, 1000)], fill="white")
    clear_draw(draw)
    draw_message(0, "Dave", "19:51", "tmrw at 11", True)
    draw_message(100, "Dylan", "18:38", "Are you here?")
    draw_message(200, "Chris", "10:12", "I think it will work.")
    draw_message(300, "Bob W7JNM", "09:23", "CW 14.035")
    epd.display_Partial(epd.getbuffer(ScreenImage1))
    epd.sleep()

    # for number, details in conversation_details.items():
    #     print(f"\nNumber: {number}")
    #     print(f"Name: {details['name']}")
    #     print("\n----")
    #print(conversation_details)

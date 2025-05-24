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

def handleSms(sms):
    print(f"Got text from {sms.number}: {sms.text}")
    store.save_message(sms.number, sms.text)
    print(store.get_all_conversations())

def init_modem():
    global modem_init
    global modem  # Declare that we are using the global variable
    print('Initializing modem...')
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.connect(PIN)
    modem.waitForNetworkCoverage(10)
    modem.smsTextMode = True
    modem_init = True
    print('Modem initialized.')

def send_text(number, text):
    print('Sending SMS to: {0}'.format(number))
    response = modem.sendSms(number, text, waitForDeliveryReport=False)
    if type(response) == SentSms:
        print('SMS Delivered.')
    else:
        print('SMS Could not be sent')

def draw_message(start_location, name, time, body):
    # Calculate positions based on the starting location
    draw.text((10, start_location), str(name), font=font(20), fill=0)
    draw.text((240, start_location), str(time), font=font(20), fill=0)
    draw.text((10, start_location + 40), str(body), font=font(20), fill=0)
    draw.line([(0, start_location + 90), (300, start_location + 90)], fill=None, width=2, joint=None)

def messages():
    global modem_init
    if modem_init == False:
        init_modem()
    
    
    
    try:
        #modem.running = True
        while True:
            # Keep the program running to listen for SMS messages
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        #modem.close()
        return



if __name__ == "__main__":
    epd.init()
    epd.Clear()
    print("Done with the clear")
    # init_modem()
    # messages()
    draw.rectangle([(0, 0), (1000, 1000)], fill="white")
    draw_message(10, "Meri", "19:51", "Woah there ;)")
    draw_message(110, "Dylan", "18:38", "Are you here?")
    epd.display_Partial(epd.getbuffer(ScreenImage1))
    epd.sleep()

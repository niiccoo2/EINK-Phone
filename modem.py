#!/usr/bin/env python

"""
Demo: Send Simple SMS Demo

Simple demo to send sms via gsmmodem package
"""
from __future__ import print_function

import logging

from gsmmodem.modem import GsmModem, SentSms  # type: ignore
import random
from func import *

# We can check using the 'mode' command in cmd
PORT = '/dev/ttyUSB2'
BAUDRATE = 115200
SMS_TEXT = "Text from E-INK Phone, number " + str(random.randint(1000, 9999))
SMS_DESTINATION = '6172060139'
PIN = None  # SIM card PIN (if any)
store = MessageStore()

def handleSms(sms):
    print(f"Got text from {sms.number}: {sms.text}")
    store.save_message(sms.number, sms.text)
    print(store.get_all_conversations())

modem = None  # Global variable to hold the modem instance

def init_modem():
    global modem  # Declare that we are using the global variable
    print('Initializing modem...')
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.connect(PIN)
    modem.waitForNetworkCoverage(10)
    modem.smsTextMode = True
    print('Modem initialized.')

def send_text(number, text):
    print('Sending SMS to: {0}'.format(number))
    response = modem.sendSms(number, text, waitForDeliveryReport=False)
    if type(response) == SentSms:
        print('SMS Delivered.')
    else:
        print('SMS Could not be sent')

def messages():
    
   
    
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
    init_modem()
    messages()

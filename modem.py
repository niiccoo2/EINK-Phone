#!/usr/bin/env python

"""
Demo: Send Simple SMS Demo

Simple demo to send sms via gsmmodem package
"""
from __future__ import print_function

import logging

from gsmmodem.modem import GsmModem, SentSms  # type: ignore
import random

# We can check using the 'mode' command in cmd
PORT = '/dev/ttyUSB2'
BAUDRATE = 115200
SMS_TEXT = "Text from E-INK Phone, number " + str(random.randint(1000, 9999))
SMS_DESTINATION = '6172060139'
PIN = None  # SIM card PIN (if any)

def handleSms(sms):
    print(f"Received SMS message from {sms.number}: {sms.text}")
    # If you want to clear the message from memory, you can delete it
    # sms.delete()

def init_modem():
    print('Initializing modem...')
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.connect(PIN)
    modem.waitForNetworkCoverage(10)
    modem.smsTextMode = True
    print('Modem initialized.')

def modem():
    
    #print('Sending SMS to: {0}'.format(SMS_DESTINATION))
    #response = modem.sendSms(SMS_DESTINATION, SMS_TEXT, waitForDeliveryReport=False)
    # if type(response) == SentSms:
    #     print('SMS Delivered.')
    # else:
    #     print('SMS Could not be sent')
    
    try:
        modem.running = True
        while True:
            # Keep the program running to listen for SMS messages
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        #modem.close()
        return



if __name__ == "__main__":
    init_modem()
    modem()  # Only runs if this file is the main script
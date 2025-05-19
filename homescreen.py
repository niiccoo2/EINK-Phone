#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = "./pic"
libdir = "./waveshare_epd"
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2_V2 # type: ignore
import time
from PIL import Image,ImageDraw,ImageFont
import random

epd = epd4in2_V2.EPD()

font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)



epd.init()
epd.Clear()

def calculate_size(text):
    bbox = draw.textbbox((0,0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return (text_width, text_height)


# while True:
messages = "Messages"
phone = "Phone"


ScreenImage1 = Image.new('1', (epd.height, epd.width), 255)  # 255: Set all pixels to white 

draw = ImageDraw.Draw(ScreenImage1)

messages_width, messages_height = calculate_size(messages)
messages_x = (300 - messages_width) // 2
draw.text((messages_x, 20), messages, font = font, fill = 0)

phone_width, phone_height = calculate_size(phone)
phone_x = (300 - phone_width) // 2
draw.text((phone_x, 100), phone, font = font, fill = 0) 

#epd.display(epd.getbuffer(ScreenImage1))
epd.display_Partial(epd.getbuffer(ScreenImage1))
    

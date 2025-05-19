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
from func import *

epd = epd4in2_V2.EPD()

font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)



epd.init()
epd.Clear()

def calculate_size(text):
    bbox = draw.textbbox((0,0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return (text_width, text_height)

apps = {
    "Messages": {
    "Name": "Messages",
    "Path": "./Messages.py",
    },
    "Phone": {
        "Name": "Phone",
        "Path": "./Phone.py",
    }
}

ScreenImage1 = Image.new('1', (epd.height, epd.width), 255)  # 255: Set all pixels to white 

draw = ImageDraw.Draw(ScreenImage1)
adding_y = -40 # The y value of apps starts x pixels from the top of the screen

for app_key in apps:
    print(app_key)
    width, height = calculate_size(apps[app_key]["Name"])
    x = (300 - width) // 2
    adding_y = adding_y + height + 40
    draw.text((x, adding_y), apps[app_key]["Name"], font = font, fill = 0) 

#epd.display(epd.getbuffer(ScreenImage1))
epd.display_Partial(epd.getbuffer(ScreenImage1))
epd.sleep()
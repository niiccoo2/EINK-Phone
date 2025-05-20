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

def draw_apps(apps):
    adding_y = -40 # The y value of apps starts x pixels from the top of the screen
    for app_key in apps:
        print(app_key)
        width, height = calculate_size(apps[app_key]["Name"])
        x = (300 - width) // 2
        adding_y = adding_y + height + 40
        draw.text((x, adding_y), apps[app_key]["Name"], font = font, fill = 0)
        apps[app_key]["Position"] = (x, adding_y)

apps = {
    "Messages": {
    "Name": "Messages",
    "Path": "./Messages.py",
    "Position": (0, 0),
    },
    "Phone": {
        "Name": "Phone",
        "Path": "./Phone.py",
        "Position": (0, 0),
    }
}

ScreenImage1 = Image.new('1', (epd.height, epd.width), 255)  # 255: Set all pixels to white 

draw = ImageDraw.Draw(ScreenImage1)
selected_index = 0
app_keys = list(apps.keys())

 ### Drawing the first screen ###
draw_apps(apps)
draw.text((45, 28), ">", font = font, fill = 0)
epd.display_Partial(epd.getbuffer(ScreenImage1))
#################################

while True:
    user_input = input("Input: ")
    # Version 1. Seems better than version 2
    draw.rectangle([(0, 0), (1000, 1000)], fill="white") # 1000, 1000, makes the white rectangle cover the entire screen
    # Version 2
    # ScreenImage1 = Image.new('1', (epd.height, epd.width), 255)  # Making a new image
    # draw = ImageDraw.Draw(ScreenImage1) # Making a new draw
    if user_input == "exit":
        break
    elif user_input == "s":
        selected_index = selected_index + 1
        if selected_index >= len(app_keys):
            selected_index = 0
    elif user_input == "w":
        selected_index = selected_index - 1
        if selected_index < 0:
            selected_index = len(app_keys) - 1
    current_app = app_keys[selected_index]
    draw.text((45, apps[current_app]["Position"][1]), ">", font = font, fill = 0)
    draw_apps(apps) 
    epd.display_Partial(epd.getbuffer(ScreenImage1))




epd.sleep()
print("Done")
exit()
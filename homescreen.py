#!/usr/bin/python
# -*- coding:utf-8 -*-
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
from modem import *

epd = epd4in2_V2.EPD()

def draw_apps(apps):
    adding_y = -40 # The y value of apps starts x pixels from the top of the screen
    for app_key in apps:
        #print(app_key)
        width, height = calculate_size(draw, apps[app_key]["Name"], font(30))
        x = (300 - width) // 2
        adding_y = adding_y + height + 40
        draw.text((x, adding_y), apps[app_key]["Name"], font = font(30), fill = 0)
        apps[app_key]["Position"] = (x, adding_y)

apps = {
    "Messages": {
        "Name": "Messages",
        "Function": messages_app,
        "Position": (0, 0),
    },
    "Phone": {
        "Name": "Phone",
        "Function": sleep,
        "Position": (0, 0),
    },
    "Sleep": {
        "Name": "Sleep",
        "Function": sleep,
        "Position": (0, 0),
    }
}

print("Initializing screen...")
ScreenImage1 = Image.new('1', (epd.height, epd.width), 255)  # 255: Set all pixels to white 

draw = ImageDraw.Draw(ScreenImage1)
selected_index = 0
app_keys = list(apps.keys())

skip_modem_init = False
epd.init()
epd.Clear()

width, height = calculate_size(draw, "Loading...", font(30))
x = (300 - width) // 2
y = (400 - height) // 2
draw.text((x, y), "Loading...", font = font(30), fill = 0) # After screen works, say loading
epd.display_Partial(epd.getbuffer(ScreenImage1))
#epd.sleep()
print('Screen initialized.\n')

if skip_modem_init == False:
    init_modem()



### Drawing the first screen ###
clear_screen()
clear_draw(draw)
draw_apps(apps)
draw.text((45, 28), ">", font = font(30), fill = 0)
epd.display_Partial(epd.getbuffer(ScreenImage1))
print("Initialization done!")
#################################

while True:
    user_input = input("Input: ")
    # draw.rectangle([(0, 0), (1000, 1000)], fill="white") # 1000, 1000, makes the white rectangle cover the entire screen
    clear_draw(draw)
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
    elif user_input == "e":
        print("Running the selected app")
        apps[app_keys[selected_index]]["Function"]()
        clear_screen()
        
    current_app = app_keys[selected_index]
    print(current_app) # Printing the selected app
    draw.text((45, apps[current_app]["Position"][1]), ">", font = font(30), fill = 0)
    draw_apps(apps) 
    epd.display_Partial(epd.getbuffer(ScreenImage1))




epd.sleep()
print("Done!")
exit()
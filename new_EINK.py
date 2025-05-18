#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = "./pic"
libdir = "./waveshare_epd"
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2_V2
import time
from PIL import Image,ImageDraw,ImageFont
import random

epd = epd4in2_V2.EPD()




epd.init()
#epd.Clear()

for i in range(10):
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    # test=input("? ")

    ScreenImage1 = Image.new('1', (epd.height, epd.width), 255)  # 255: Set all pixels to white 
        
    draw = ImageDraw.Draw(ScreenImage1)
    draw.text((10, 0), str(random.randint(1000,100000000)), font = font35, fill = 0)

    print("Refresh")
    epd.display(epd.getbuffer(ScreenImage1))


print("Done!")
epd.sleep()
epd4in2_V2.epdconfig.module_exit(cleanup=True)
exit()
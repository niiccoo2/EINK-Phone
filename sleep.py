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

epd.init()
epd.Clear()
epd.sleep()
epd4in2_V2.epdconfig.module_exit(cleanup=True)
print("Done!")
exit()
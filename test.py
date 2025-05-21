#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = "./pic"
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

font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)

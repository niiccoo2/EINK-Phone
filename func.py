import sys
import os
from waveshare_epd import epd4in2_V2
import time
from PIL import Image,ImageDraw,ImageFont



def clear_screen():
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()

def sleep():
    epd = epd4in2_V2.EPD()

    epd.init()
    epd.Clear()
    epd.sleep()
    epd4in2_V2.epdconfig.module_exit(cleanup=True)
    print("Done!")
    exit()

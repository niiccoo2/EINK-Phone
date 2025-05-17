from eink_ui import EInkUI
from components import Label
import epd4in2_V2  # Your driver

epd = epd4in2_V2.EPD()
epd.init()

ui = EInkUI(400, 300)
ui.add(Label(10, 10, "Nico is cool!"))
ui.draw_all()

epd.display_partial(epd.getbuffer(ui.get_image()))

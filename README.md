[Google Doc Notes Link](https://docs.google.com/document/d/1l_P9BNs8-fzjLHjxsxwmtQVHC8uADbmZvHsqvaNpZNw/edit?usp=sharing)
[Docs link for pico version](https://docs.google.com/document/d/1WdVnLDW4LZ5mjuCLy1hVp1n7MNubI6F_SzgGbY42siQ/edit?usp=sharing)

### Sunday, May 11:
* Saw the light phone 3 and thought it cost too much.
* Started thinking about how I could make my own

*30 minutes*

### Monday, May 12:
* Decided to use a pi zero w
* Ordered a SIM7600A-H cell modem.

*30 minutes*

### Thursday, May 15:
* Got modem and started working on the python code that sends texts
* Found out that verizon does not work with my modem
* Thought that ssh was slow bc I was using a pi zero *My fault not true*
* Ordered rpi zero 2w
* Ordered a new sim card
* Ordered a 4.2in Waveshare E-Ink screen

*5 hours*

### Saturday, May 17:
* Started figuring out how to use the display drivers in python
* Got the demo working [Photo](https://photos.app.goo.gl/T3E3aoRRHVqETAhi7)
* Got it so that it would display a random number
* Figured out how to use partial refreshes

*4 hours*

### Sunday, May 18:
*Got a basic homescreen working it will dynamically display apps from a dictionary

*3 hours*

### Tuesday, May 20:
*Added a cursor so you can use input statements to move up and down on the screen and select an app. [Photo](https://photos.app.goo.gl/G6LSFMMkUEmNv3iD8)

*3 hours*

### Thursday, May 22:
* Set up new sim card
* FINALLY got the modem working for texting and data
* Hardwired the usb connection because the cable was too big
* [Blog Post](https://niiccoo2.xyz/raspberry-pi-modems/)

*4 hours*

### Friday, May 23:
* Somehow corrupted my pc by thruning on bluetooth, all I wanted was music
* Started working on the first screen of the messages app [Photo](https://photos.app.goo.gl/84rxM1MTwXnvZ23s9)

*4 hours*

### Saturday, May 24:
* Made it so the convos would dynamically display from the JSON file. [Photo](https://photos.app.goo.gl/KQzkmpvL8ekmdxA4A)
* I (Think?) I added scrolling to the convo view today (still has bugs)

*4 hours*

### Sunday, May 25:
* Added the message view
* Made it so it will refresh if you get a new message or send one
* Saves sent and recived messages to the JSON file
* TEXT WRAPPING!!!
* Write text to the left OR the right side of the screen. [Photo](https://photos.app.goo.gl/zQqkJZknWvvdAGR4A)

*6 hours*

### Monday, May 26:
* Made a bad YouTube video about the phone, got almost 3k views for first video

### Thursday, May 29:
* Added scrolling to the message view
* Got idea to make custom PCB for the keyboard

*2 hours*

### Friday, May 30:
* Started learning KiCad and designing the PCB schematic

*5 hours*

### Saturday, May 31:
* HACKNIGHT!
* Worked on the Keyboard pcb a bit

*1 hour*

### Sunday, June 1:
* HACKNIGHT!

### Monday June 2:
* Wired the PCB in KiCad
* Ordered PCB from PcbWay
* Ordered parts from digikey
* Forgot power connecter on PCB (Not the end of the world)

*4 hours*

### Saturday, June 7:
* Tried to get the modem to call my phone, having issues
* Made an account on some b2b site to update firmware.

*2 hours*

# Highway project starts here:
I worked on this a bunch with my own time and money. I got a ok prototype but I'm deciding to change to a custom pcb and using the SIM7000G so that the final device will be much smaller.

### Tuesday, June 17:
* Decided to change from using a pi zero 2 to a pi pico
* Pi pico will use much less power
* Using a SIM7000G modem
* Making a custom PCB
import sys
import smbus
import time
import RPi.GPIO as GPIO

# Default I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

bus = smbus.SMBus(1)

def set_color(r,g,b):
    "Set backlight color to (Red,Green,Blue), where R, G, and B range from 0 to 255."
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 1, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x08, 0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 4, r)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 3, g)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 2, b)

def set_text(text):
    "Set display text with auto-wrap. Only 32 characters can be shown."
    
    # Clear display
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, 0x01)
    time.sleep(.05)
    
    # Turn on display with no cursor
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, 0x0c)
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, 0x28)
    time.sleep(.05)
    
    # Iterate over input text, moving to the next row if first is full
    count = 0
    row = 0
    for c in text:
	
	# If moving to the next row, add a newline to the display
	# If we've filled two rows, break early.
        if c == '\n' or count == 16:
            count = 0
            row = row + 1
            if row >= 2:
                break
            bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, 0xc0)
	    
	    # Don't increment count or display character if it's a newline character
            if c == '\n':
                continue
		
        count = count + 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))

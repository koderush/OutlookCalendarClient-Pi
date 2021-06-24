#!/usr/bin/env python
import time

from Adafruit_LED_Backpack import AlphaNum4


# Create display instance on default I2C address (0x70) and bus number.
display0 = AlphaNum4.AlphaNum4()

# Alternatively, create a display with a specific I2C address and/or bus.
display1 = AlphaNum4.AlphaNum4(address=0x71, busnum=1)

# Scroll a message across the display
message = 'VACATION'

# Initialize the display. Must be called once before using the display.
display0.begin()
display1.begin()

# Clear the display buffer.
display0.clear()
display1.clear()

# Print a 4 character string to the display buffer.
display0.print_str(message[0:4])
display1.print_str(message[4:8])

# Write the display buffer to the hardware.  This must be called to
# update the actual display LEDs.
display0.write_display()
display1.write_display()


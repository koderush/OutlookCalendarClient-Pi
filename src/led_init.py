import time

from Adafruit_LED_Backpack import AlphaNum4


# Create display instance on default I2C address (0x70) and bus number.
display0 = AlphaNum4.AlphaNum4()

# Alternatively, create a display with a specific I2C address and/or bus.
display1 = AlphaNum4.AlphaNum4(address=0x71, busnum=1)

# Initialize the display. Must be called once before using the display.
display0.begin()
display1.begin()


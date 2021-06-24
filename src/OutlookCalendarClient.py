#!/usr/bin/env python
import sys
import urllib2
import datetime
import time

from Adafruit_LED_Backpack import AlphaNum4

global g_led_0
global g_led_1
global g_calendarItems
global g_counter
global g_text

CALENDAR_SERVER = "http://kyou-w7.int.pason.com:8777/outlookcalendar"
CALENDAR_UPDATE_SCHEDULE = datetime.timedelta(0,15) # (day,second)
CODE_MEETING = -1000
CODE_USE_CALENDAR_SUBJECT = -2000
MESSAGE_MEETING = 'MEETING '
FLAG_USE_CALENDAR_TEXT = '^^'
BUSY_SYMBOLS = ['|','/','-','\\']

class CalendarItem:
    start = ''
    startTimestamp = 0
    end = ''
    endTimestamp = 0
    subject = ''
    location = ''

    def parse( self, line ):
        fields = line.split('|')

        self.start = fields[0]
        self.startTimestamp = int(fields[1])
        self.end = fields[2]
        self.endTimestamp = int(fields[3])
        self.subject = fields[4]
        self.location = fields[5]

def timestampToDatetime( timestamp ):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

# returns seconds to the event
# returns 0 if in a event
# returns negative value for special use
def toNextEvent(timestamp):
    global g_text
    
    current = datetime.datetime.now()

    #if((current.hour < 7) or (current.hour >= 16)):
    #   return CODE_OFF_WORK

    timeToNextEvent = 9999999

    for item in g_calendarItems:
        # Skip ended events
        if(item.endTimestamp <= timestamp):
            continue

        # In event
        if((item.startTimestamp < timestamp) and (item.endTimestamp > timestamp)):
            if(item.subject[:2] == FLAG_USE_CALENDAR_TEXT):
                g_text = item.subject[2:]
                return CODE_USE_CALENDAR_SUBJECT
            else:
                return CODE_MEETING
        # Look for the next event
        elif((item.startTimestamp - timestamp) < timeToNextEvent):
            timeToNextEvent = item.startTimestamp - timestamp

    return timeToNextEvent


def updateCalendar():
    try:
        calendar = urllib2.urlopen( CALENDAR_SERVER ).read()
    except:
        print "Error in getting calendar(" + str(datetime.datetime.now()) + ")"
        return

    global g_calendarItems
    del g_calendarItems[:]

    calendarLines = calendar.splitlines(True);

    for line in calendarLines:
        item = CalendarItem()
        item.parse( line )
        g_calendarItems.append( item )

    print 'Sync Outlook Calendar(' + str(datetime.datetime.now()) + ' ' + str(len(g_calendarItems)) + ' items)'

def printLED(message):
    # Clear the display buffer.
    g_led_0.clear()
    g_led_1.clear()

    # Print a 4 character string to the display buffer.
    g_led_0.print_str(message[0:4])
    g_led_1.print_str(message[4:8])


    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    g_led_0.write_display()
    g_led_1.write_display()

def printDotFlow():
    pos = g_counter % 8
    
    for i in range(4):
        g_led_0.set_decimal(i, (pos == i))
        g_led_1.set_decimal(i, ((pos - 4) == i))

    g_led_0.write_display()
    g_led_1.write_display()

def printDot(pos):
    onOff = (g_counter % 2 == 1)
    if(pos < 3):
        g_led_0.set_decimal(pos, onOff)
        g_led_0.write_display()
    else:
        g_led_1.set_decimal((pos-4), onOff)
        g_led_1.write_display()

def printBusy(pos):
    symbol = BUSY_SYMBOLS[g_counter % 4]
    if(pos < 3):
        g_led_0.set_digit(pos, symbol)
        g_led_0.write_display()
    else:
        g_led_1.set_digit((pos-4), symbol)
        g_led_1.write_display()
        
def formatMessage(timeToNext):
    if(timeToNext == CODE_USE_CALENDAR_SUBJECT):
        return g_text
    elif(timeToNext == CODE_MEETING):
        return MESSAGE_MEETING
    else:
        hour = int(timeToNext/3600)
        minute = int((timeToNext-hour*3600)/60)
        second = timeToNext%60
        return str(hour) + '-' + str(minute) + '-' + str(second)


## Main section:

# Create display instance on default I2C address (0x70) and bus number.
g_led_0 = AlphaNum4.AlphaNum4()

# Alternatively, create a display with a specific I2C address and/or bus.
g_led_1 = AlphaNum4.AlphaNum4(address=0x71, busnum=1)

# Initialize the display. Must be called once before using the display.
g_led_0.begin()
g_led_1.begin()

# Clear the display buffer.
g_led_0.clear()
g_led_1.clear()

g_calendarItems = []

g_counter = 0

g_text = '++++++++'

updateCalendar()

calendarLastUpdate = datetime.datetime.now()

while True:
    g_counter += 1

    timeDelta = datetime.datetime.now() - calendarLastUpdate

    if( timeDelta > CALENDAR_UPDATE_SCHEDULE ):
        updateCalendar()
        calendarLastUpdate = datetime.datetime.now()

    nextEvent = toNextEvent(int(time.time()))

    printLED(formatMessage(nextEvent))

    if(nextEvent == CODE_MEETING):
        printBusy(7)
        # printDot(7)
            
    # printDotFlow()

    time.sleep(0.25)

#End Main section


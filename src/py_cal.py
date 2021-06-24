#!/usr/bin/env python
import urllib2

class CalendarItem:
    start = ""
    end = ""
    subject = ""
    location = ""
    
    def parse( self, line ):
        fields = line.split('|')
        
        self.start = fields[0]
        self.end = fields[1]
        self.subject = fields[2]
        self.location = fields[3]
    
    
calendar = urllib2.urlopen("http://kyou-w7.int.pason.com:8777/outlookcalendar").read()

calendarLines = calendar.splitlines(True);

calendarItemList = []

for line in calendarLines:
    item = CalendarItem()
    item.parse( line )
    calendarItemList.append( item )


for item in calendarItemList:
    print '[' + item.start + '][' + item.end + '][' + item.subject + '][' + item.location + ']'



import re
import datetime
import time

class Event:
    '''todo: remove redundancy in data?'''
    def __init__(self, content = None, type = None, startDate = None, endDate = None):
        self.content = content
        self.type = type
        
        if startDate is not None:
            self.startDate = startDate
            self.startYear = startDate.year
            self.startMonth = startDate.month
            self.startDay = startDate.day

            self.endDate = endDate if endDate is not None else startDate
            self.endYear = endDate.year if endDate is not None else startDate.year
            self.endMonth = endDate.month if endDate is not None else startDate.month
            self.endDay = endDate.day if endDate is not None else startDate.day
            
    def __str__(self):
    	if self.startDate == self.endDate:
    	    return self.startDate.strftime('%Y-%m-%d') + ' : ' + self.type + ' : ' + self.content
    	else:
    	    return self.startDate.strftime('%Y-%m-%d') + '-' + self.endDate.strftime('%Y-%m-%d') + ' : ' + self.type + ' : ' + self.content
            
class TextFileParser:
  
    def __init__(self):
        self.ignoredLineRegex = re.compile('^\s*$|^\s*\#.*$') # ignore empty lines and comments
        self.validEventLineRegex = re.compile("^(?P<startYear>\d{4})-(?P<startMonth>\d{2})-(?P<startDay>\d{2})\s*" 
            + "(-\s*(?P<endYear>\d{4})-(?P<endMonth>\d{2})-(?P<endDay>\d{2})\s*)?" 
            + ":\s*"
            + "(?P<type>\w+)\s*"
            + ":\s*"
            + "(?P<event>.*)$", re.VERBOSE)
  
    def readFiles(self, files):
        lines = []
        for filename in files:
            for line in open(filename):
                lines.append(unicode(line, 'utf-8'))
                
        return self.readLines(lines)
  
    def readLines(self, lines):
        return [self.parseLine(line) for line in lines if line != "" and self.ignoredLineRegex.match(line) is None]
  
    def parseLine(self, line):        
        matcher = self.validEventLineRegex.match(line)
        if matcher is None:
            raise Exception('Line not matched: ' + line)

        event = Event()

        event.startYear = matcher.group('startYear')
        event.startMonth = matcher.group('startMonth')
        event.startDay = matcher.group('startDay')

        event.endYear = matcher.group('endYear')
        event.endMonth = matcher.group('endMonth')
        event.endDay = matcher.group('endDay')

        event.content = matcher.group('event')
        event.type = matcher.group('type')

        try:
            event.startDate = datetime.date(int(event.startYear), int(event.startMonth), int(event.startDay))        
        except ValueError: 
            raise ValueError("Could not parse start date: %s-%s-%s" % (event.startYear, event.startMonth, event.startDay))
    
        if event.endYear != None and event.endMonth != None and event.endDay != None:
            try:
                event.endDate = datetime.date(int(event.endYear), int(event.endMonth), int(event.endDay))        
            except ValueError: 
                raise ValueError("Could not parse end date: %d-%d-%d" % (int(event.endYear), int(event.endMonth), int(event.endDay)))
                
            if event.startDate > event.endDate:
                raise ValueError('Start date after end date')                
        else:
            event.endDate = event.startDate

        return event

    
class SimpleEventFilter: 
  
    def getEvents(self, events, type, date):
        selectedEvents = [event for event in events if event.type == type and self.showEvent(event, date)]
        return sorted(selectedEvents, key=lambda event: event.startDate)

    def showEvent(self, tokens, date):
        return self.isDateWithinRange(tokens.startDate, tokens.endDate, date)

    def isDateWithinRange(self, start, end, date):
        startDayMonth = (start.month, start.day)
        endDayMonth = (end.month, end.day)
        dateDayMonth = (date.month, date.day)

        if start.year == end.year:
            return startDayMonth <= dateDayMonth <= endDayMonth
        elif start.year + 1 == end.year:
            return (start.year == date.year and startDayMonth <= dateDayMonth) or (date.year == end.year and dateDayMonth <= endDayMonth)
        else:
            raise ValueError('Not more than one year difference between event start and end is allowed')        
    

class GetClosestEventsFilter(SimpleEventFilter):
    '''if the number of todays events is lower than given eventCount value, fill the list with other events by proximity'''

    def __init__(self, eventCount):
        self.eventCount = eventCount

    def getEvents(self, events, type, date):
        events = [event for event in events if event.type == type]
        # this can be optimized:
        events = sorted(map(lambda event: (self.dateDistance(date, event), event), events)) 
        #events = sorted(events, key=lambda event: self.dateDistance(date, event))
        selectedEvents = []
        counter = 0
        for (diff, event) in events:
            if diff == 0 or counter < self.eventCount:
                selectedEvents.append(event)
                counter += 1
            else:
                break
                    
        return sorted(selectedEvents, key=lambda event: event.startYear)
            
    def dateDistance(self, date, event):

        # not very pretty
        if event.endDate.year == date.year:
            return 1000

        startDayMonth = (event.startDate.month, event.startDate.day)
        endDayMonth = (event.endDate.month, event.endDate.day)
        dateDayMonth = (date.month, date.day)

        if startDayMonth < dateDayMonth and dateDayMonth < endDayMonth:
            return 0
        elif startDayMonth > dateDayMonth:
            return self.dayMonthDifference(startDayMonth, dateDayMonth)
        else:
            return self.dayMonthDifference(dateDayMonth, endDayMonth)

    def dayMonthDifference(self, dayMonthTouple1, dayMonthTouple2):
        if dayMonthTouple1 > dayMonthTouple2:
            bigger = dayMonthTouple1
            smaller = dayMonthTouple2
        else:
	    bigger = dayMonthTouple2
	    smaller = dayMonthTouple1
	    
        return 31*(bigger[0] - smaller[0]) + (bigger[1] - smaller[1])
        

class Model:

    def __init__(self, parser, textFilter, imageFilter, files):
        self.parser = parser
        self.textFilter = textFilter
        self.imageFilter = imageFilter
        self.allowedTypes = ['text', 'image']
        self.files = files
        
    def getEventsForDate(self, date):
        events = self.parser.readFiles(self.files)
        eventWithUnsupportedType = next((event for event in events if event.type not in self.allowedTypes), None)
        if eventWithUnsupportedType is not None:
            raise Exception('Unsupported event type: ' + eventWithUnsupportedType.type)
        
        result = {
	  'text' : self.textFilter.getEvents(events, 'text', date),
	  'image' : self.imageFilter.getEvents(events, 'image', date)
	}
	return result
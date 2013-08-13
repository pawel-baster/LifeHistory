
import re
import datetime

class Event:

    def __init__(self, eventName = None, type = None, startDate = None, endDate = None):
        self.eventName = eventName
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
            
class TextFileParser:
  
    def __init__(self, files):
        self.lines = []
        self.files = files
        self.ignoredLineRegex = re.compile('^\s*$|^\s*\#.*$') # ignore empty lines and comments
        self.validEventLineRegex = re.compile("^(?P<startYear>\d{4})-(?P<startMonth>\d{2})-(?P<startDay>\d{2})\s*" 
            + "(-\s*(?P<endYear>\d{4})-(?P<endMonth>\d{2})-(?P<endDay>\d{2})\s*)?" 
            + ":\s*"
            + "(?P<type>\w+)\s*"
            + ":\s*"
            + "(?P<event>.*)$", re.VERBOSE)
  
    def parseLine(self, line):        
        matcher = self.validEventLineRegex.match(line)
        if matcher is None:
            raise Exception('Line not matched: ' + line)

        tokens = Event()

        tokens.startYear = matcher.group('startYear')
        tokens.startMonth = matcher.group('startMonth')
        tokens.startDay = matcher.group('startDay')

        tokens.endYear = matcher.group('endYear')
        tokens.endMonth = matcher.group('endMonth')
        tokens.endDay = matcher.group('endDay')

        tokens.eventName = matcher.group('event')
        tokens.type = matcher.group('type')

        try:
            tokens.startDate = datetime.date(int(tokens.startYear), int(tokens.startMonth), int(tokens.startDay))        
        except ValueError: 
            raise ValueError("Could not parse start date: %s-%s-%s" % (tokens.startYear, tokens.startMonth, tokens.startDay))
    
        if tokens.endYear != None and tokens.endMonth != None and tokens.endDay != None:
            try:
                tokens.endDate = datetime.date(int(tokens.endYear), int(tokens.endMonth), int(tokens.endDay))        
            except ValueError: 
                raise ValueError("Could not parse end date: %d-%d-%d" % (int(tokens.endYear), int(tokens.endMonth), int(tokens.endDay)))
                
            if tokens.startDate > tokens.endDate:
                raise ValueError('Start date after end date')                
        else:
            tokens.endDate = tokens.startDate

        return tokens
            
    def reloadEvents(self):
        self.lines = []
        for filename in self.files:
            for line in open(filename):
              self.addLine(line)

    def addLines(self, lines):
        for line in lines:
            self.addLine(line)
    
    def addLine(self, line):
        if line != "" and self.ignoredLineRegex.match(line) is None:
            self.lines.append(line)

    def getEvents(self):
        events = []
        for line in self.lines:
            eventTokens = self.parseLine(line)
            events.append(eventTokens)
        return events

    
class Model: 

    def __init__(self, parser):
        self.parser = parser
      
    def getEvents(self, type, date, reload=False):
        if reload:
            self.parser.reloadEvents()
        events = []
        for event in self.parser.getEvents():
            if event.type == type and self.showEvent(event, date):
                events.append(event)
        return sorted(events, key=lambda event: event.startDate)

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
    

class GetClosestEventsModel(Model):
    '''if the number of todays events is lower than given eventCount value, fill the list with other events by proximity'''

    def __init__(self, parser, eventCount):
        Model.__init__(self, parser)
        self.eventCount = eventCount

    def getEvents(self, type, date, reload=False):
        if reload:
            self.parser.reloadEvents()
        events = [event for event in self.parser.getEvents() if event.type == type]
        events = sorted(map(lambda event: (self.dateDistance(date, event), event), events)) 
        selectedEvents = []
        counter = 0
        for (diff, event) in events:
            if diff == 0 or counter < self.eventCount:
                selectedEvents.append(event)
                counter += 1
            else:
                break
                    
        return sorted(selectedEvents, key=lambda event: event.startDate)
            
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
        return 31*(dayMonthTouple1[0] - dayMonthTouple2[0]) + (dayMonthTouple1[1] - dayMonthTouple2[1])

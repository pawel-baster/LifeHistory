
import re
import datetime

class LineTokens:
	eventName = None

	startYear = None
	startMonth = None
	startDay = None
	startDate = None

	endYear = None
	endMonth = None
	endDay = None
	endDate = None

class FileParser:
  
	def __init__(self, files):
		self.lines = []
		self.files = files
		self.ignoredLineRegex = re.compile('^\s*$|^\s*\#.*$') # ignore empty lines and comments
		self.validEventLineRegex = re.compile("^(?P<startYear>\d{4})-(?P<startMonth>\d{2})-(?P<startDay>\d{2})\s*" 
			+ "(-\s*(?P<endYear>\d{4})-(?P<endMonth>\d{2})-(?P<endDay>\d{2})\s*)?" 
			+ ":\s*" 
			+ "(?P<event>.*)$", re.VERBOSE)
  
	def parseLine(self, line):		
		matcher = self.validEventLineRegex.match(line)
		if matcher is None:
			raise Exception('Line not matched: ' + line)

		tokens = LineTokens()

		tokens.startYear = matcher.group('startYear')
		tokens.startMonth = matcher.group('startMonth')
		tokens.startDay = matcher.group('startDay')

		tokens.endYear = matcher.group('endYear')
		tokens.endMonth = matcher.group('endMonth')
		tokens.endDay = matcher.group('endDay')

		tokens.eventName = matcher.group('event')
		return tokens
	        
	def reloadEvents(self):
		self.lines = []
		for filename in self.files:
		    for line in open(filename):
			  self.addLine(line)
		
	def addLine(self, line):
		if line != "" and self.ignoredLineRegex.match(line) is None:
			self.lines.append(line)

	def getEventsFromLoadedFiles(self, date):
		return self.getEvents(self.lines, date)

	def getEvents(self, date):
		events = []
		for line in self.lines:
			eventTokens = self.parseLine(line)
			#if self.showEvent(eventTokens, date):
			events.append(eventTokens)
		return events

	
class Model: 

	def __init__(self, parser):
		self.parser = parser
	  
	def getEvents(self, date):
		self.parser.reloadEvents()
		events = []
		for eventTokens in self.parser.getEvents(date):
		    if self.showEvent(eventTokens, date):
			events.append(eventTokens)
		return sorted(events, key=lambda event: event.startDate)
		
	def showEvent(self, tokens, today):
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

		return self.isDateWithinRange(tokens.startDate, tokens.endDate, today)

	def isDateWithinRange(self, start, end, date):
		startTouple = (start.month, start.day)
		endTouple = (end.month, end.day)
		curTouple = (date.month, date.day)

		if start.year == end.year:
			return startTouple <= curTouple <= endTouple
		elif start.year + 1 == end.year:
			return (start.year == date.year and startTouple <= curTouple) or (date.year == end.year and curTouple <= endTouple)
		else:
			raise ValueError('Not more than one year difference between event start and end is allowed')		
	

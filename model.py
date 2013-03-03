
import re
import datetime

class LineTokens:
	isComment = None
	name = None

	startYear = None
	startMonth = None
	startDay = None
	startDate = None

	endYear = None
	endMonth = None
	endDay = None
	endDate = None

class Model: 

	def getEvents(self, lines, date):
		events = []
		for line in lines:
			eventTokens = self.parseLine(line)
			if self.showEvent(eventTokens, date):
				events.append((eventTokens.startYear, eventTokens.event))
		
				
		return events

	def parseLine(self, line):
		pattern = re.compile("^(?P<comment>\#).*"
			+ "|(?P<startYear>\d{4})-(?P<startMonth>\d{2})-(?P<startDay>\d{2})\s*" 
			+ "(-\s*(?P<endYear>\d{4})-(?P<endMonth>\d{2})-(?P<endDay>\d{2})\s*)?" 
			+ ":\s*" 
			+ "(?P<event>.*)$", re.VERBOSE)
		matcher = pattern.match(line)
		if matcher is None:
			raise Exception('Line not matched: ' + line)

		tokens = LineTokens()

		tokens.isComment = (matcher.group('comment') == '#')

		tokens.startYear = matcher.group('startYear')
		tokens.startMonth = matcher.group('startMonth')
		tokens.startDay = matcher.group('startDay')

		tokens.endYear = matcher.group('endYear')
		tokens.endMonth = matcher.group('endMonth')
		tokens.endDay = matcher.group('endDay')

		tokens.event = matcher.group('event')
		return tokens
		
	def showEvent(self, tokens, today):
		if tokens.isComment:
			return False

		tokens.startDate = datetime.date(int(tokens.startYear), int(tokens.startMonth), int(tokens.startDay))		
		if tokens.endYear != None and tokens.endMonth != None and tokens.endDay != None:
			tokens.endDate = datetime.date(int(tokens.endYear), int(tokens.endMonth), int(tokens.endDay))		
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
	

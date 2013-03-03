
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
			if self.validateTokens(eventTokens):
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

	def validateTokens(self, tokens):
		if tokens.isComment:
			return False

		tokens.startDate = datetime.date(int(tokens.startYear), int(tokens.startMonth), int(tokens.startDay))		
		if tokens.endYear != None and tokens.endMonth != None and tokens.endDay != None:
			tokens.startDate = datetime.date(int(tokens.endYear), int(tokens.endMonth), int(tokens.endDay))		
			assert tokens.endDate != None, "tokens == None, " + str(tokens)
		else:
			tokens.endDate = tokens.startDate
			assert tokens.endDate != None, "tokens == None, " + str(tokens)
		return True
		
	def showEvent(self, tokens, today):
		if self.dateWithinRange(tokens.startDate, tokens.endDate, today):
			return True
		else:
			return False

	def dateWithinRange(self, start, end, date):
		startTouple = (start.month, start.day)
		endTouple = (end.month, end.day)
		curTouple = (date.month, date.day)

		return startTouple <= curTouple <= endTouple
		

import unittest
import datetime
from model import TextFileParser, Model, Event, GetClosestEventsModel

class TextFileParserTest(unittest.TestCase):

    def testLineRead(self):
	"""single line"""
	parser = TextFileParser([])
	eventLine1 = '2012-02-20: Event 1'
	parser.addLine(eventLine1)
	assert len(parser.lines) == 1
	assert parser.lines[0] == eventLine1

    def testEmptyLinesAndComments(self):
        """empty lines and comments"""
	parser = TextFileParser([])
	parser.addLine('')
	parser.addLine(' ')
	parser.addLine(' # comment')
	parser.addLine('# comment')
        eventLine = '2012-02-20 : Test event'
	parser.addLine(eventLine)
	assert len(parser.lines) == 1
	assert parser.lines[0] == eventLine

    def testParseEvent(self):
	parser = TextFileParser([])
	event =	parser.parseLine('2012-02-20: Event 1')
	assert event.eventName == 'Event 1'
	assert event.startYear == '2012'
 	assert event.startMonth == '02'
 	assert event.startDay == '20'
 	assert event.endYear == None
 	assert event.endMonth == None
 	assert event.endDay == None

    def testParseMultiDayEvent(self):
	parser = TextFileParser([])
	event =	parser.parseLine('2012-02-21 - 2012-02-22: Event 1')
	assert event.eventName == 'Event 1'
	assert event.startYear == '2012'
 	assert event.startMonth == '02'
 	assert event.startDay == '21'
 	assert event.endYear == '2012'
 	assert event.endMonth == '02'
 	assert event.endDay == '22'

    def testInvalidDateHandling(self):
	parser = TextFileParser([])
	try:
    	    event = parser.parseLine('2012-02-22 - 2012-02-20: Event 1')	
	except ValueError:
	    return
	assert False

class MockParser:
    
   def __init__(self, events):
	self.events = events

   def getEvents(self):
	return self.events

class ModelTest(unittest.TestCase):

    def testGetEvent(self):
	"""Test returning one day events"""
	events = [Event('Single event 1', datetime.date(2012, 2, 20)),
		Event('Single event 2', datetime.date(2012, 2, 20)),
		Event('Single event 3', datetime.date(2012, 2, 21))]
	parser = MockParser(events)
	model = Model(parser)
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 19))) == 0
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 20))) == 2, "Expected %d, got %d" % (2, len(events2))
	events3 = model.readEventsFromParser(datetime.date(2012, 2, 21))
	assert len(events3) == 1
	assert events3[0].eventName == 'Single event 3'
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 22))) == 0

    def testGetEvent2(self):
	"""Test retrieving multi day events"""
	events = [Event('Single event 1', datetime.date(2012, 2, 10), datetime.date(2012, 2, 20)),
		Event('Single event 2', datetime.date(2012, 2, 15), datetime.date(2012, 2, 25)),
		Event('Single event 3', datetime.date(2012, 2, 20), datetime.date(2012, 2, 26))]
	parser = MockParser(events)
	model = Model(parser)

	assert len(model.readEventsFromParser(datetime.date(2012, 2, 9))) == 0
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 10))) == 1
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 15))) == 2
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 20))) == 3
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 25))) == 2
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 26))) == 1
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 27))) == 0
	
    def testGetEvent3(self):
	"""Test retrieving a multi-day event when it has different start and end dates"""
	events = [Event('Single event 1', datetime.date(2011, 12, 1), datetime.date(2012, 1, 30))]
	parser = MockParser(events)
	model = Model(parser)

	assert len(model.readEventsFromParser(datetime.date(2011, 11, 30))) == 0
	assert len(model.readEventsFromParser(datetime.date(2011, 12, 1))) == 1
	assert len(model.readEventsFromParser(datetime.date(2011, 12, 31))) == 1
	assert len(model.readEventsFromParser(datetime.date(2012, 1, 1))) == 1
	assert len(model.readEventsFromParser(datetime.date(2012, 1, 30))) == 1
	assert len(model.readEventsFromParser(datetime.date(2012, 2, 1))) == 0
	assert len(model.readEventsFromParser(datetime.date(2012, 12, 1))) == 0

class GetClosestEventsModelTest(unittest.TestCase):

    def testRetrievingEvents(self):
	"""Test retrieving events from other dates if found less events than eventCount"""
	events = [Event('Single event 1', datetime.date(2012, 2, 10)),
	    Event('Single event 2', datetime.date(2012, 2, 11)),
	    Event('Single event 3', datetime.date(2012, 2, 12))]

	parser = MockParser(events)
	eventCount = 2
	model = GetClosestEventsModel(parser, eventCount)

	# should return 2 regardless of the date
	events = model.readEventsFromParser(datetime.date(2012, 12, 10))
	assert len(events) == eventCount, "Expected %d, got: %d" % (eventCount, len(events))
	assert events[0].eventName == 'Single event 1'
	assert events[1].eventName == 'Single event 2'
	assert len(model.readEventsFromParser(datetime.date(2012, 12, 11))) == eventCount
	assert len(model.readEventsFromParser(datetime.date(2012, 12, 12))) == eventCount
	assert len(model.readEventsFromParser(datetime.date(2012, 12, 13))) == eventCount

if __name__ == "__main__":
    unittest.main() # run all tests

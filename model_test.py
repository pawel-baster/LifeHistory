import unittest
import datetime
from model import TextFileParser, GetClosestEventsFilter, Event, SimpleEventFilter, Model

class EventTest(unittest.TestCase):
	
    def testToString(self):
    	event = Event('event', 'text', datetime.date(2012, 2, 21))
    	self.assertEquals('2012-02-21 : text : event', str(event))
    	
    def testToString(self):
    	event = Event('event', 'text', datetime.date(2012, 2, 21), datetime.date(2012, 2, 22))
    	self.assertEquals('2012-02-21-2012-02-22 : text : event', str(event))

class TextFileParserTest(unittest.TestCase):

    def testLineRead(self):
        """single line"""
        parser = TextFileParser()
        eventLine1 = '2012-02-20 : type : Event 1'
        events = parser.readLines([eventLine1])
        self.assertEquals(1, len(events))
        self.assertEquals('Event 1', events[0].content)

    def testEmptyLinesAndComments(self):
        """empty lines and comments"""
        parser = TextFileParser()
        eventLine = '2012-02-20 : type : Test event'
        events = parser.readLines(['', ' ', ' # comment', '#comment', eventLine])
        self.assertEquals(1, len(events))
        self.assertEquals('Test event', events[0].content)

    def testParseEvent(self):
        parser = TextFileParser()
        event = parser.parseLine('2012-02-20 : type : Event 1')
        self.assertEquals('Event 1', event.content)
        self.assertEquals('type', event.type, event.type)
        self.assertEquals('2012' , event.startYear)
        self.assertEquals('02', event.startMonth)
        self.assertEquals('20', event.startDay)
        self.assertEquals(None, event.endYear)
        self.assertEquals(None, event.endMonth)
        self.assertEquals(None, event.endDay)

    def testParseMultiDayEvent(self):
        parser = TextFileParser()
        event = parser.parseLine('2012-02-21 - 2012-02-22: type : Event 1')
        self.assertEquals('Event 1', event.content)
        self.assertEquals('type', event.type)
        self.assertEquals('2012', event.startYear)
        self.assertEquals('02', event.startMonth)
        self.assertEquals('21', event.startDay)
        self.assertEquals('2012', event.endYear)
        self.assertEquals('02', event.endMonth)
        self.assertEquals('22', event.endDay)

    def testInvalidDateHandling(self):
        parser = TextFileParser()
        try:
            event = parser.parseLine('2012-02-22 - 2012-02-20 : type : Event 1')    
        except ValueError:
            return
        assert False

class SimpleEventFilterTest(unittest.TestCase):

    def testGetEvent(self):
        """Test returning one day events"""
        type = 'type1'
        events = [Event('Single event 1', type, datetime.date(2012, 2, 20)),
            Event('Single event 2', type, datetime.date(2012, 2, 20)),
            Event('Single event 3', type, datetime.date(2012, 2, 21))]
        filter = SimpleEventFilter()
        self.assertEquals(0, len(filter.getEvents(events, type, datetime.date(2012, 2, 19))))
        self.assertEquals(2, len(filter.getEvents(events, type, datetime.date(2012, 2, 20))))
        events3 = filter.getEvents(events, type, datetime.date(2012, 2, 21))
        self.assertEquals(1, len(events3))
        self.assertEquals('Single event 3', events3[0].content)
        self.assertEquals(0, len(filter.getEvents(events, type, datetime.date(2012, 2, 22))))

    def testGetEventDifferentCategories(self):
        """Test retrieving from different types"""
        events = [Event('Single event 1', 'type1', datetime.date(2012, 2, 20)),
            Event('Single event 2', 'type2', datetime.date(2012, 2, 20))]
        filter = SimpleEventFilter()
        self.assertEquals(1, len(filter.getEvents(events, 'type1', datetime.date(2012, 2, 20))))
        self.assertEquals(1, len(filter.getEvents(events, 'type2', datetime.date(2012, 2, 20))))
        self.assertEquals(0, len(filter.getEvents(events, 'type3', datetime.date(2012, 2, 20))))

    def testGetEvent2(self):
        """Test retrieving multi day events"""
        type = 'type1'
        events = [Event('Single event 1', type, datetime.date(2012, 2, 10), datetime.date(2012, 2, 20)),
        Event('Single event 2', type, datetime.date(2012, 2, 15), datetime.date(2012, 2, 25)),
        Event('Single event 3', type, datetime.date(2012, 2, 20), datetime.date(2012, 2, 26))]
        filter = SimpleEventFilter()
        #print filter.getEvents(events, type, datetime.date(2012, 2, 10))['type1']
        self.assertEquals(0, len(filter.getEvents(events, type, datetime.date(2012, 2, 9))))
        self.assertEquals(1, len(filter.getEvents(events, type, datetime.date(2012, 2, 10))))
        self.assertEquals(2, len(filter.getEvents(events, type, datetime.date(2012, 2, 15))))
        self.assertEquals(3, len(filter.getEvents(events, type, datetime.date(2012, 2, 20))))
        self.assertEquals(2, len(filter.getEvents(events, type, datetime.date(2012, 2, 25))))
        self.assertEquals(1, len(filter.getEvents(events, type, datetime.date(2012, 2, 26))))
        self.assertEquals(0, len(filter.getEvents(events, type, datetime.date(2012, 2, 27))))
    
    def testGetEvent3(self):
        """Test retrieving a multi-day event when it has different start and end dates"""
        type = 'type1'
        events = [Event('Single event 1', type, datetime.date(2011, 12, 1), datetime.date(2012, 1, 30))]
        filter = SimpleEventFilter()

        self.assertEquals(0, len(filter.getEvents(events, type, datetime.date(2011, 11, 30))))
        self.assertEquals(1, len(filter.getEvents(events, type, datetime.date(2011, 12, 1))))
        self.assertEquals(1, len(filter.getEvents(events, type, datetime.date(2011, 12, 31))))
        self.assertEquals(1, len(filter.getEvents(events, type, datetime.date(2012, 1, 1))))
        self.assertEquals(1, len(filter.getEvents(events, type, datetime.date(2012, 1, 30))))
        self.assertEquals(0, len(filter.getEvents(events, type, datetime.date(2012, 2, 1))))
        self.assertEquals(0, len(filter.getEvents(events, type, datetime.date(2012, 12, 1))))
    
    def testGetEvent4(self):
        """Test that events come in a right order"""
        type = 'type1'
        events = [Event('Single event 3', type, datetime.date(2012, 1, 1)),
            Event('Single event 2', type, datetime.date(2011, 1, 1)),
            Event('Single event 1', type, datetime.date(2010, 1, 1))]
        filter = SimpleEventFilter()
        events = filter.getEvents(events, type, datetime.date(2013, 1, 1))
        self.assertEquals(3, len(events))
        self.assertEquals('Single event 1', events[0].content)
        self.assertEquals('Single event 2', events[1].content)
        self.assertEquals('Single event 3', events[2].content)

class GetClosestEventsFilterTest(unittest.TestCase):

    def testRetrievingEvents(self):
        """Test retrieving events from other dates if found less events than eventCount"""
        type = 'type1'
        events = [Event('Single event 1', type, datetime.date(2012, 2, 10)),
            Event('Single event 2', type, datetime.date(2012, 2, 11)),
            Event('Single event 3', type, datetime.date(2012, 2, 8)),
            Event('Single event 4', type, datetime.date(2012, 2, 13)),
            Event('Single event 5', type, datetime.date(2012, 2, 14))]

        eventCount = 4
        filter = GetClosestEventsFilter(eventCount)

        # should return 2 regardless of the date
        events = filter.getEvents(events, type, datetime.date(2013, 2, 10))
        self.assertEquals(eventCount, len(events))
        self.assertEquals('Single event 1', events[0].content)
        self.assertEquals('Single event 2', events[1].content)
        self.assertEquals('Single event 3', events[2].content)
        self.assertEquals('Single event 4', events[3].content)
        self.assertEquals(eventCount, len(filter.getEvents(events, type, datetime.date(2012, 12, 11))))
        self.assertEquals(eventCount, len(filter.getEvents(events, type, datetime.date(2012, 12, 12))))
        self.assertEquals(eventCount, len(filter.getEvents(events, type, datetime.date(2012, 12, 13))))

class MockParser(TextFileParser):
    
    def __init__(self, events):
        self.events = events
    
    def readFiles(self, files):
        return self.events

class ModelTest(unittest.TestCase):
  
    def testErrorOnCategoryNotAllowed(self):
        mockParser = MockParser([Event('Unsupportd', 'new-type', datetime.date(2012, 12, 10))])
        filter = SimpleEventFilter()
        model = Model(mockParser, filter, filter, [])
        self.assertRaises(Exception, model.getEventsForDate, datetime.date(2012, 12, 10))
        model.allowedTypes = ['new-type']
        model.getEventsForDate(datetime.date(2012, 12, 10))
        
        

if __name__ == "__main__":
    unittest.main() # run all tests

import unittest
import datetime
from model import TextFileParser, GetClosestEventsFilter, Event, SimpleEventFilter

class TextFileParserTest(unittest.TestCase):

    def testLineRead(self):
        """single line"""
        parser = TextFileParser([])
        eventLine1 = '2012-02-20 : type : Event 1'
        parser.addLine(eventLine1)
        self.assertEquals(1, len(parser.lines))
        self.assertEquals(eventLine1, parser.lines[0])

    def testEmptyLinesAndComments(self):
        """empty lines and comments"""
        parser = TextFileParser([])
        parser.addLine('')
        parser.addLine(' ')
        parser.addLine(' # comment')
        parser.addLine('# comment')
        eventLine = '2012-02-20 : type : Test event'
        parser.addLine(eventLine)
        self.assertEquals(1, len(parser.lines))
        self.assertEquals(eventLine, parser.lines[0])

    def testParseEvent(self):
        parser = TextFileParser([])
        event = parser.parseLine('2012-02-20 : type : Event 1')
        self.assertEquals('Event 1', event.eventName)
        self.assertEquals('type', event.type, event.type)
        self.assertEquals('2012' , event.startYear)
        self.assertEquals('02', event.startMonth)
        self.assertEquals('20', event.startDay)
        self.assertEquals(None, event.endYear)
        self.assertEquals(None, event.endMonth)
        self.assertEquals(None, event.endDay)

    def testParseMultiDayEvent(self):
        parser = TextFileParser([])
        event = parser.parseLine('2012-02-21 - 2012-02-22: type : Event 1')
        self.assertEquals('Event 1', event.eventName)
        self.assertEquals('type', event.type)
        self.assertEquals('2012', event.startYear)
        self.assertEquals('02', event.startMonth)
        self.assertEquals('21', event.startDay)
        self.assertEquals('2012', event.endYear)
        self.assertEquals('02', event.endMonth)
        self.assertEquals('22', event.endDay)

    def testInvalidDateHandling(self):
        parser = TextFileParser([])
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
        self.assertEquals('Single event 3', events3[0].eventName)
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
        self.assertEquals('Single event 1', events[0].eventName)
        self.assertEquals('Single event 2', events[1].eventName)
        self.assertEquals('Single event 3', events[2].eventName)

class GetClosestEventsFilterTest(unittest.TestCase):

    def testRetrievingEvents(self):
        """Test retrieving events from other dates if found less events than eventCount"""
        type = 'type1'
        events = [Event('Single event 1', type, datetime.date(2012, 2, 10)),
            Event('Single event 2', type, datetime.date(2012, 2, 11)),
            Event('Single event 3', type, datetime.date(2012, 2, 12))]

        eventCount = 2
        filter = GetClosestEventsFilter(eventCount)

        # should return 2 regardless of the date
        events = filter.getEvents(events, type, datetime.date(2012, 12, 10))
        self.assertEquals(eventCount, len(events))
        self.assertEquals('Single event 1', events[0].eventName)
        self.assertEquals('Single event 2', events[1].eventName)
        self.assertEquals(eventCount, len(filter.getEvents(events, type, datetime.date(2012, 12, 11))))
        self.assertEquals(eventCount, len(filter.getEvents(events, type, datetime.date(2012, 12, 12))))
        self.assertEquals(eventCount, len(filter.getEvents(events, type, datetime.date(2012, 12, 13))))

if __name__ == "__main__":
    unittest.main() # run all tests

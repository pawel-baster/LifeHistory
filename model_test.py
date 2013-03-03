import unittest
import datetime
from model import Model

class ModelTestCase(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.instance = Model()

    def testGetEvents(self):
        """Single event"""
        lines = ['2012-02-20: Event 1']
	events = self.instance.getEvents(lines, datetime.date(2012, 2, 20))
	assert len(events) == 1, "expected %d, got: %d" % (1, len(events))
	assert events[0] == ('2012', 'Event 1'), "got: " + ", ".join(events[0])

    def testGetEvents2(self):
        """No events on that day"""
        lines = ['2012-02-19: Event1']
	events = self.instance.getEvents(lines, datetime.date(2012, 2, 20))
	assert len(events) == 0, "expected %d results, got: %d" % (0, len(events))

    def testGetEvents3(self):
        """empty events list"""
        lines = []
	events = self.instance.getEvents(lines, datetime.date(2012, 2, 20))
	assert len(events) == 0

    def testGetEvents4(self):
        """three events, two at the same date"""
        lines = ['2012-02-20: Event 1', '2012-02-21: Overlapping event 1', '2012-02-21: Overlapping event 2']
	events1 = self.instance.getEvents(lines, datetime.date(2012, 2, 20))
	assert len(events1) == 1
	assert events1[0] == ('2012', 'Event 1')
	events2 = self.instance.getEvents(lines, datetime.date(2012, 2, 21))
	assert len(events2) == 2
	assert events2[0] == ('2012', 'Overlapping event 1')
	assert events2[1] == ('2012', 'Overlapping event 2')

    def testGetEvents5(self):
        """Test comments"""
        lines = ['# a comment', '2012-02-20: Event 1']
	events = self.instance.getEvents(lines, datetime.date(2012, 2, 20))
	assert len(events) == 1
	assert events[0] == ('2012', 'Event 1')

    def testGetEvents6(self):
	"""Test multiple day events"""
	lines = ['2012-02-10 - 2012-02-20: Event 1', '2012-02-15-2012-02-25: Event 2']

	events1 = self.instance.getEvents(lines, datetime.date(2012, 2, 5))
	assert len(events1) == 0
	
	events2 = self.instance.getEvents(lines, datetime.date(2012, 2, 15))
	assert len(events2) == 1
	assert events2[0] == ('2012', 'Event 1')

	events3 = self.instance.getEvents(lines, datetime.date(2012, 2, 18))
	assert len(events3) == 2
	assert events3[0] == ('2012', 'Event 1')
	assert events3[1] == ('2012', 'Event 2')

	events4 = self.instance.getEvents(lines, datetime.date(2012, 2, 22))
	assert len(events4) == 1
	assert events4[0] == ('2012', 'Event 2')

	events5 = self.instance.getEvents(lines, datetime.date(2012, 2, 26))
	assert len(events5) == 0

    def testGetEvents7(self):
	"""Test multiple day event with invalid dates"""
	lines = ['2012-02-20 - 2012-02-10: Event 1']

	events1 = self.instance.getEvents(lines, datetime.date(2012, 2, 5))
	assert False

    def testGetEvents8(self):
	"""Test multiple day event with different start and end year"""
	lines = ['2011-12-30 - 2012-01-02: Event 1']
	events = self.instance.getEvents(lines, datetime.date(2011, 12, 31))
	assert len(events) == 1
	events = self.instance.getEvents(lines, datetime.date(2012, 12, 31))
	assert len(events) == 0
	events = self.instance.getEvents(lines, datetime.date(2012, 01, 01))
	assert len(events) == 1
	events = self.instance.getEvents(lines, datetime.date(2011, 01, 01))
	assert len(events) == 0


if __name__ == "__main__":
    unittest.main() # run all tests

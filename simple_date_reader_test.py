import unittest
import datetime
from scan_folders_controller import SimpleDateReader

class SimpleDateReaderTest(unittest.TestCase):
	
    def testGetDateFromPath(self): 
    	path = "/home/user/Pictures/2013/2013-06-08 Event/Pano.jpg"
    	instance = SimpleDateReader()
    	self.assertEquals(datetime.datetime(2013, 6, 8, 0, 0), instance.getDateFromPath(path))
    	
    def testGetDateFromPath2(self): 
    	path = "/home/user/Pictures/2010/Trip (17.04.10)/29817.jpg"
    	instance = SimpleDateReader()
    	self.assertEquals(datetime.datetime(2010, 4, 17, 0, 0), instance.getDateFromPath(path))  	
    	
    def testGetDateFromPathError(self): 
    	path = "/home/user/Pictures/2013/2013-13-08 Event/Pano.jpg"
    	instance = SimpleDateReader()
    	self.assertRaises(ValueError, instance.getDateFromPath, path)

if __name__ == "__main__":
    unittest.main() # run all tests

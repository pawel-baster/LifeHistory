import unittest
import time
from date_extractor import ImageDateExtractor

class ImageDateExtractorTest(unittest.TestCase):
	
    def testGetDateFromPath(self): 
    	path = "/home/user/Pictures/2013/2013-06-08 Event/Pano.jpg"
    	instance = ImageDateExtractor()
    	self.assertEquals(time.strptime('08-06-2013', '%d-%m-%Y'), instance.getDateFromPath(path))
    	
    def testGetDateFromPath2(self): 
    	path = "/home/user/Pictures/2010/Trip (17.04.10)/29817.jpg"
    	instance = ImageDateExtractor()
    	self.assertEquals(time.strptime('17-04-2010', '%d-%m-%Y'), instance.getDateFromPath(path))  	
    	
    def testGetDateFromPathError(self): 
    	path = "/home/user/Pictures/2013/2013-13-08 Event/Pano.jpg"
    	instance = ImageDateExtractor()
    	self.assertRaises(ValueError, instance.getDateFromPath, path)

if __name__ == "__main__":
    unittest.main() # run all tests

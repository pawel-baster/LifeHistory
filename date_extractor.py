import os
import time
import fnmatch
import sys
from PIL import Image
from PIL.ExifTags import TAGS

class ExifReader:

    def get_exif_data(self, fname):
        """Get embedded EXIF data from image file."""
        ret = {}
        try:
            img = Image.open(fname)
            if hasattr( img, '_getexif' ):
                exifinfo = img._getexif()
                if exifinfo != None:
                    for tag, value in exifinfo.items():
                        decoded = TAGS.get(tag, tag)
                        ret[decoded] = value
        except IOError:
            print 'IOERROR ' + fname
        return ret

class ImageDateExtractor:

    def __init__(self):    
        self.er = ExifReader() # TODO remove tight coupling 

    def extractDates(self, path):
    
        for dirpath, dirnames, files in os.walk(path):
           for f in fnmatch.filter(files, '*.jpg'):
               path = os.path.join(dirpath, f) 
               date = self.getDate(path)
               if date is not None:
                   print time.strftime("%Y-%m-%d", date) + ' : image : ' + path
               else:
                   print '# Could not extract date from: ' + path

    def getDate(self, path):
        try:
            exifData = self.er.get_exif_data(path)
            if 'DateTimeOriginal' in exifData:
                return self.parseDate(exifData['DateTimeOriginal'])
            if 'DateTimeDigitized' in exifData:
                return self.parseDate(exifData['DateTimeDigitized'])
            return None
        except:
	    return None
        
    def parseDate(self, string):
        try:
	    return time.strptime(string, "%Y:%m:%d %H:%M:%S")
	except ValueError:
	    return time.strptime(string, "%Y/%m/%d %H:%M:%S")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        extractor = ImageDateExtractor()
        extractor.extractDates(sys.argv[1])
    else:
        print "please pass the folder as the only argument"

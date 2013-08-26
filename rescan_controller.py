from PIL import Image
from PIL.ExifTags import TAGS

import os
import fnmatch
import time
import datetime

class RescanController:
   
    def __init__(self, folders, parser, date_reader):
        self.folders = folders
        self.parser = parser
        self.date_reader = date_reader
     
    def rescan_all(self):
        for folder in self.folders:
            self.rescan_folder(folder, self.folders[folder])
           
    def rescan_folder(self, folder, filename):
       hash = self.load_into_dictionary(filename)
          
       result = self.traverse_folder(hash, folder)    
       imagesWithDates = result[0]
       imagesWithoutDates = result[1]
       
       for path, dt_obj in imagesWithDates:
           event = Event(path, 'image', dt_obj)
	   print event
      
      # foreach image in images_without_dates:
          # try to retrieve it from the directory name
          # display a dialog
          
      # save file

    def traverse_folder(self, hash, folder):
        imagesWithDates = []
        imagesWithoutDates = []
        for dirpath, dirnames, files in os.walk(folder):
           for f in [f for f in files if fnmatch.fnmatch(f.lower(), '*.jpg')]: 
               path = os.path.join(dirpath, f) 
               date = self.date_reader.get_date(path)
               if date is not None:
		   print "got date for " + path
                   dt_obj = datetime.datetime.fromtimestamp(time.mktime(date))
                   imagesWithDates.append((path, dt_obj))
               else:
                   imagesWithoutDates.append(path)
                   print "no date for " + path
                   
        return (imagesWithDates, imagesWithoutDates)

    def load_into_dictionary(self, filename):
        hash = {}
        if os.path.exists(filename):
            events = parser.readFiles([filename])
            for event in events:
                if event.type == 'image':
                    hash[event.content] = event.startDate
        return hash
       
class SimpleDateReader:
    
    def get_date(self, path):
        #try:
            exifData = self.get_exif_data(path)
            if 'DateTimeOriginal' in exifData:
                return self.parse_date(exifData['DateTimeOriginal'])
            if 'DateTimeDigitized' in exifData:
                return self.parse_date(exifData['DateTimeDigitized'])
            #date = self.getDateFromPath(path)
            #if date is not None:
            #	return date
            return None
        #except:
	#    return None
    
    def get_exif_data(self, fname):
        """Get embedded EXIF data from image file."""
        ret = {}
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
        return ret
      
    def parse_date(self, string):
        try:
	    return time.strptime(string, "%Y:%m:%d %H:%M:%S")
	except ValueError:
	    return time.strptime(string, "%Y/%m/%d %H:%M:%S")

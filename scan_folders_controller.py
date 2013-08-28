from PIL import Image
from PIL.ExifTags import TAGS

import wx
import os
import fnmatch
import time
import datetime

from model import Event
from scan_dialog import DatePickerDialog

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
       
       lines = []
       
       for path, dt_obj in imagesWithDates:
           event = Event(path, 'image', dt_obj)
           lines.append(str(event))
       
       userDates = self.promptForDates(imagesWithoutDates)
       
       for path, date in userDates:
           if date is not None:
               event = Event(path, 'image', date)
               lines.append(str(event))
           else:
               lines.append("# Could not find date for " + path)
               
       with open(filename, 'w') as f:
           for line in lines:
               f.write(line + "\n")

    def promptForDates(self, images):
         imageList = map(lambda path: (path, None), images)
         app = wx.PySimpleApp(0)
         wx.InitAllImageHandlers()
         dialog_1 = DatePickerDialog(imageList, None, -1, "")
         app.SetTopWindow(dialog_1)
         dialog_1.Show()
         app.MainLoop()
         return imageList

    def traverse_folder(self, hash, folder):
        imagesWithDates = []
        imagesWithoutDates = []
        for dirpath, dirnames, files in os.walk(folder):
           for f in [f for f in files if fnmatch.fnmatch(f.lower(), '*.jpg')]: 
               path = os.path.join(dirpath, f) 
               date = self.date_reader.get_date(path)
               if date is not None:
                   dt_obj = datetime.datetime.fromtimestamp(time.mktime(date))
                   imagesWithDates.append((path, dt_obj))
               elif path in hash:
                   imagesWithDates.append((path, hash[path]))
               else:
                   imagesWithoutDates.append(path)
                   
        return (imagesWithDates, imagesWithoutDates)

    def load_into_dictionary(self, filename):
        hash = {}
        if os.path.exists(filename):
            events = self.parser.readFiles([filename])
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
        formats = ["%Y:%m:%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"]
        for format in formats:
            try:
                return time.strptime(string, format)
            except ValueError:
                pass
        return None

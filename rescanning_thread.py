# coding=UTF-8

import threading
import time
import wx
import os
import fnmatch
import datetime
import re

from helpers import ExifHelper
from model import Event

class RescanningThread(threading.Thread):
  
    def __init__(self, folders, parser, date_reader):
        threading.Thread.__init__(self)
        self.folders = folders
        self.parser = parser
        self.date_reader = date_reader
  
    def start_if_needed(self):
        self.start()
    
    def run(self):
        time.sleep(300)
        for folder in self.folders:
           self.rescan_folder(folder, self.folders[folder])
           
    def rescan_folder(self, folder, filename):
        hash = self.load_into_dictionary(filename)
        print "found %d events in file %s" % (len(hash), filename)   
        
        for key in hash:
            print type(key)
            break
          
        if not os.path.exists(folder):
            raise Exception("Folder %s does not exist" % folder)
	 
        result = self.traverse_folder(hash, folder)    
        imagesWithDates = result[0]
        imagesWithoutDates = result[1]
        newCount = result[2]
      
        print "found %d images with dates, %d imgages without dates, new: %d" % (len(imagesWithDates), len(imagesWithoutDates), newCount)
      
        if newCount == 0:
            # no need to update
            return
      
        lines = []
      
        for path, dt_obj in imagesWithDates:
            event = Event(path.encode('utf-8'), 'image', dt_obj)
            lines.append(str(event))
       
        for image in imagesWithoutDates:
            lines.append("# Could not find date for " + path)
       
       #if len(imagesWithoutDates) > 0:
       #    userDates = self.promptForDates(imagesWithoutDates)
       
       #    for path, date in userDates:
       #        if date is not None:
       #           event = Event(path, 'image', date)
       #           lines.append(str(event))
       #        else:
       #           lines.append("# Could not find date for " + path)
               
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line + "\n")
       
        print "Updated file: %s (saved %d lines)" % (filename, len(lines))

    #def promptForDates(self, images):
    #     imageList = map(lambda path: (path, self.date_reader.get_date_from_path(path)), images)
    #     app = wx.PySimpleApp(0)
    #     wx.InitAllImageHandlers()
    #     dialog_1 = DatePickerDialog(imageList, None, -1, "")
    #     app.SetTopWindow(dialog_1)
    #     dialog_1.Show()
    #     app.MainLoop()
    #     return imageList

    def traverse_folder(self, hash, folder):
        imagesWithDates = []
        imagesWithoutDates = []
        newCount = 0
        for dirpath, dirnames, files in os.walk(folder):
           for f in sorted([f for f in files if fnmatch.fnmatch(f.lower(), '*.jpg')]): 
               path = os.path.join(dirpath, f).decode('utf-8')               
               if path in hash:
                   imagesWithDates.append((path, hash[path]))
               else:
		   newCount = newCount + 1
                   date = self.date_reader.get_date(path)
                   if date is not None:
                       dt_obj = datetime.datetime.fromtimestamp(time.mktime(date))
                       imagesWithDates.append((path, dt_obj))
                       print "Found new file with exif data: " + path                       
                   else:
                       imagesWithoutDates.append(path)
                       print "Found new file without exif data: " + path       
                   
        return (imagesWithDates, imagesWithoutDates, newCount)

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
        try:
            exifData = ExifHelper.get_exif_data(path)
            if 'DateTimeOriginal' in exifData:
                return self.parse_date(exifData['DateTimeOriginal'])
            if 'DateTimeDigitized' in exifData:
                return self.parse_date(exifData['DateTimeDigitized'])
            return None
        except IOError as e:
	    print "Error while reading EXIF data from %s: %s" % (path, e.strerror)
	    return None
    
    def parse_date(self, string):
        formats = ["%Y:%m:%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"]
        for format in formats:
            try:
                return time.strptime(string, format)
            except ValueError:
                pass
        return None
        
    def get_date_from_path(self, path):
    	dirname = os.path.basename(os.path.dirname(path))
    	regexps = [('(\d{4}-\d{2}-\d{2})', '%Y-%m-%d'),
    	    ('(\d{2}\.\d{2}\.\d{2})', '%d.%m.%y')]
    	for regexp, date_format in regexps:
    	    matcher = re.search(regexp, path)
            if matcher is not None:
               return datetime.datetime.strptime(matcher.group(0), date_format)
    	return None
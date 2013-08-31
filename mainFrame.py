#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 on Fri Aug 16 08:06:53 2013

import wx
import wx.grid
import datetime
import random
from helpers import ExifHelper

import config

# begin wxGlade: extracode
# end wxGlade


class LifeHistoryMainFrame(wx.Frame):
    def __init__(self, model, *args, **kwds):
        self.model = model
        # begin wxGlade: LifeHistoryMainFrame.__init__
        kwds["style"] = wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR | wx.CLIP_CHILDREN
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        self.image = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.btnPrev = wx.Button(self, -1, "<")
        self.imageCounter = wx.StaticText(self, -1, "0/1")
        self.btnNext = wx.Button(self, -1, ">")
        self.imageDescription = wx.StaticText(self, -1, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onPrevImage, self.btnPrev)
        self.Bind(wx.EVT_BUTTON, self.onNextImage, self.btnNext)
        # end wxGlade
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onNextImage, self.timer)
        self.timer.Start(config.slideshowInterval * 1000)
        
    def __set_properties(self):
        # begin wxGlade: LifeHistoryMainFrame.__set_properties
        self.SetTitle("Life History")
        self.SetSize((400, 534))
        self.panel_1.SetScrollRate(10, 10)
        # end wxGlade
        # TODO: reload every x minutes
        
    def __do_layout(self):
        # begin wxGlade: LifeHistoryMainFrame.__do_layout
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        textEventHolder = wx.BoxSizer(wx.VERTICAL)
        self.panel_1.SetSizer(textEventHolder)
        sizer_5.Add(self.panel_1, 1, wx.EXPAND, 0)
        sizer_7.Add(self.image, 0, 0, 0)
        sizer_5.Add(sizer_7, 0, 0, 0)
        sizer_6.Add(self.btnPrev, 0, 0, 0)
        sizer_6.Add(self.imageCounter, 0, wx.ALL, 5)
        sizer_6.Add(self.btnNext, 0, 0, 0)
        sizer_6.Add(self.imageDescription, 0, wx.ALL, 5)
        sizer_5.Add(sizer_6, 0, 0, 0)
        self.SetSizer(sizer_5)
        self.Layout()
        self.Centre()
        # end wxGlade
        self.textEventHolder = textEventHolder
        self.updateEvents()
        
    def updateEvents(self):
    	print 'reading events...'
        events = self.model.getEventsForDate(datetime.date.today())
        self.displayTextEvents(events['text'])
        self.registerImageEvents(events['image'])
                
    def registerImageEvents(self, imageEvents):
        self.imageList = imageEvents
        if len(self.imageList ) > 0:
            self.pictureId = 0
            self.displaySelectedImage()
            self.SetSizeHints(minW=400, maxW=400, minH=400)
        else:
            self.image.Hide()
            self.btnPrev.Hide()
            self.btnNext.Hide()
            self.imageCounter.Hide()
            self.SetSizeHints(minW=400, maxW=400, minH=200)
            self.SetSize((400, 300))	

    def displayTextEvents(self, events):
    	#self.panel.DestroyChildren()
        for event in events:
            yearLabel = wx.StaticText(self.panel_1, -1, str(event.startDate))
            eventTextLabel = wx.StaticText(self.panel_1, -1, event.content)
            eventTextLabel.Wrap(self.GetSize().width - 120)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(yearLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            sizer.Add(eventTextLabel, 0, wx.ALL, 5)
            self.textEventHolder.Add(sizer, 0, 0, 11)

    def displaySelectedImage(self):
        filename = self.imageList[self.pictureId].content
        image = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        image = self.rotateByExif(filename, image)
        image = self.scaleImage(image)        
        self.image.SetBitmap(wx.BitmapFromImage(image))
        self.imageCounter.SetLabel("%d / %d" % (self.pictureId + 1, len(self.imageList)))
        self.imageDescription.SetLabel(str(self.imageList[self.pictureId].startDate))
        # TODO: center the bitmap
            
    def rotateByExif(self, path, image):
    	'''rotates the image (if needed) using exif orientation data'''
    	exif_data = ExifHelper.get_exif_data(path)
    	#print exif_data
    	if 'Orientation' in exif_data:
    	    orientation = exif_data['Orientation']
    	    print 'orientation: ' + str(orientation)
    	    if orientation == 6:
    	        return image.Rotate90()
    	else: 
    	    print 'no orientation data'
    	return image
    
    def scaleImage(self, img):        
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            PhotoMaxSize = self.GetSize().width
            NewW = PhotoMaxSize
            NewH = PhotoMaxSize * H / W
        else:
            PhotoMaxSize = self.GetSize().width * 0.75
            NewH = PhotoMaxSize
            NewW = PhotoMaxSize * W / H
        return img.Scale(NewW,NewH)

    def onPrevImage(self, event):  # wxGlade: LifeHistoryMainFrame.<event_handler>
        self.pictureId = self.pictureId - 1 if self.pictureId > 0 else len(self.imageList) - 1
        self.displaySelectedImage()

    def onNextImage(self, event):  # wxGlade: LifeHistoryMainFrame.<event_handler>
        self.pictureId = self.pictureId + 1 if self.pictureId < len(self.imageList) - 1 else 0
        self.displaySelectedImage()

# end of class LifeHistoryMainFrame
class LifeHistoryApp(wx.App):
    def __init__(self, arg, model):
        self.model = model
        wx.App.__init__(self, arg)        
  
    def OnInit(self):
        wx.InitAllImageHandlers()
        mainFrame = LifeHistoryMainFrame(self.model, None, -1, "")
        self.SetTopWindow(mainFrame)
        mainFrame.Show()
        return 1

# end of class LifeHistoryApp
import wx
import config
import datetime
import random

class MainWindow( wx.Frame ) :

    def __init__(self, view):
        self.view = view
        
        style = (wx.DEFAULT_FRAME_STYLE ^ wx.MINIMIZE_BOX ^ wx.MAXIMIZE_BOX | wx.FRAME_NO_TASKBAR)
        wx.Frame.__init__(self, None, title='LifeHistory', style = style)
        self.SetSize( (320, 250) )
        self.SetPosition( (400, 300) )
        
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.topSizer)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(config.refreshRate * 1000)
        
        self.eventWidgets = []
        

    def showEvents(self, events, images):

        self.panel.DestroyChildren()
        
        for event in events:
            year = wx.StaticText(self.panel, label=str(event.startDate))
            event = wx.StaticText(self.panel, label=event.content)
            event.Wrap(self.GetSize().width - 80)
            rowSizer = wx.BoxSizer(wx.HORIZONTAL)
            rowSizer.Add(year, 0, wx.ALL, border=5)
            rowSizer.Add(event, 0, wx.ALL, border=5)
            self.topSizer.Add(rowSizer, 0, wx.ALL)
            self.eventWidgets.append(year)
            self.eventWidgets.append(event)
         
        if len(images) > 0:
	    random.shuffle(images)
	    image = images.pop()
            img = self.scaleImage(image.content)
            imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
            self.topSizer.Add(imageCtrl, 0, wx.ALL, border=5)
                 
        self.topSizer.Layout()
    
    def scaleImage(self, filename):
        img = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        PhotoMaxSize = self.GetSize().width
        if W > H:
            NewW = PhotoMaxSize
            NewH = PhotoMaxSize * H / W
        else:
            NewH = PhotoMaxSize
            NewW = PhotoMaxSize * W / H
        return img.Scale(NewW,NewH)
    
    def update(self, event):
          self.view.updateEventsView()

class View:
    def __init__(self, model):
        self.model = model
  
    def show(self):
        try:
            self.app = wx.App( False )
            self.frame = MainWindow(self)
            self.updateEventsView()
            self.frame.Show()
            self.app.MainLoop()
        except Exception, e:
	    wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
        
    def updateEventsView(self):
        events = self.model.getEventsForDate(datetime.date.today())
        self.frame.showEvents(events['text'], events['image'])
        #print events['image']
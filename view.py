import wx
import config
import datetime

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
		

	def showEvents(self, events):

		self.panel.DestroyChildren()
		
		for event in events:
			year = wx.StaticText(self.panel, label=str(event.startDate))
			event = wx.StaticText(self.panel, label=event.eventName)
			event.Wrap(self.GetSize().width - 50)
			rowSizer = wx.BoxSizer(wx.HORIZONTAL)
			rowSizer.Add(year, 0, wx.ALL, border=5)
			rowSizer.Add(event, 0, wx.ALL, border=5)
			self.topSizer.Add(rowSizer, 0, wx.ALL)
			self.eventWidgets.append(year)
			self.eventWidgets.append(event)
		 
		self.topSizer.Layout()
	
	def update(self, event):
	      self.view.updateEventsView()

class View:
	def __init__(self, model):
		self.model = model
  
	def show(self):
		self.app = wx.App( False )
		self.frame = MainWindow(self)				
		self.updateEventsView()
		self.frame.Show()
		self.app.MainLoop()
		
	def updateEventsView(self):
		events = self.model.getEvents(datetime.date.today())
		self.frame.showEvents(events)



import wx

class MainWindow( wx.Frame ) :

	def __init__(self):
		style = (wx.DEFAULT_FRAME_STYLE ^ wx.MINIMIZE_BOX ^ wx.MAXIMIZE_BOX | wx.FRAME_NO_TASKBAR)
		wx.Frame.__init__(self, None, title='LifeHistory', style = style)
		self.SetSize( (200, 250) )
		self.SetPosition( (400,300) )

	def showEvents(self, events):
		panel = wx.Panel(self, wx.ID_ANY)
		topSizer = wx.BoxSizer(wx.VERTICAL)
		for event in events:
			year = wx.StaticText(panel, label=event[0])
			event = wx.StaticText(panel, label=event[1])
			rowSizer = wx.BoxSizer(wx.HORIZONTAL)
			rowSizer.Add(year, 0, wx.ALL, border=5)
			rowSizer.Add(event, 0, wx.ALL, border=5)
			topSizer.Add(rowSizer, 0, wx.ALL)
		panel.SetSizer(topSizer)
	
class View:
	def show(self):
		self.app = wx.App( False )
		self.frame = MainWindow()				
		self.frame.showEvents(self.events)
		self.frame.Show()
		self.app.MainLoop()
		


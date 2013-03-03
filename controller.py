import wx
from model import Model
from view import MainWindow

class Controller:
	
	def run(self):
		app = wx.App( False )
		frame = MainWindow()
		events = [('2010', 'Event 1'), ('2011', 'Event 2')]
		frame.showEvents(events)
		frame.Show()
		app.MainLoop()

if __name__ == '__main__':
	controller = Controller()
	controller.run()


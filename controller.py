import wx
import datetime

from model import Model
from view import View
import config

class Controller:
	
	def __init__(self, model, view):
		self.model = model
		self.view = view

	def run(self):
		for filename in config.eventFiles:
			self.model.loadFile(filename)			

		view.events = self.model.getEventsFromLoadedFiles(datetime.date.today())
		view.show()

if __name__ == '__main__':
	model = Model()
	view = View()
	controller = Controller(model, view)
	controller.run()


import wx
import datetime

from model import GetClosestEventsModel, TextFileParser
from view import View
import config

class Controller:
	
	def __init__(self, model, view):
		self.model = model
		self.view = view

	def run(self):
		view.show()

if __name__ == '__main__':
	parser = TextFileParser(config.eventFiles)
	model = GetClosestEventsModel(parser, config.minNumberOfEvents)
	view = View(model)
	controller = Controller(model, view)
	controller.run()


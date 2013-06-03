import wx
import datetime

from model import Model, FileParser
from view import View
import config

class Controller:
	
	def __init__(self, model, view):
		self.model = model
		self.view = view

	def run(self):
		view.show()

if __name__ == '__main__':
	parser = FileParser(config.eventFiles)
	model = Model(parser)
	view = View(model)
	controller = Controller(model, view)
	controller.run()


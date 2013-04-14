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
		self.model.loadFiles(config.eventFiles)
		view.show()

if __name__ == '__main__':
	model = Model()
	view = View(model)
	controller = Controller(model, view)
	controller.run()


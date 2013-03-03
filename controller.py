import wx
from model import Model
from view import View

class Controller:
	
	def __init__(self, model, view):
		self.model = model
		self.view = view

	def run(self):
		events = [('2010', 'Event 1'), ('2011', 'Event 2')]
		view.events = events
		view.show()

if __name__ == '__main__':
	model = Model()
	view = View()
	controller = Controller(model, view)
	controller.run()


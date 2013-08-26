import sys
import wx
import datetime

from model import GetClosestEventsFilter, SimpleEventFilter, Model, TextFileParser
#from view import View
from mainFrame import LifeHistoryApp
import config

class Controller:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        view.show()

if __name__ == '__main__':
    parser = TextFileParser()
    if len(sys.argv) == 1:
        textFilter = GetClosestEventsFilter(config.minNumberOfEvents)
        imageFilter = SimpleEventFilter()
        model = Model(parser, textFilter, imageFilter, config.eventFiles)
        LifeHistory = LifeHistoryApp(0, model)
        LifeHistory.MainLoop()
    elif len(sys.argv) == 2 and sys.argv[1] == 'rescan':
        controller = RescanController(config.imageFolders, parser)
        controller.rescan()
    else:
        print 'incorrect arguments'




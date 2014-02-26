import sys
import wx
import datetime

from model import GetClosestEventsFilter, SimpleEventFilter, Model, TextFileParser
from rescanning_thread import RescanningThread, SimpleDateReader
from main_frame import LifeHistoryApp
import config

class Controller:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        view.show()

if __name__ == '__main__':
    parser = TextFileParser()
    textFilter = GetClosestEventsFilter(config.minNumberOfEvents)
    imageFilter = GetClosestEventsFilter(1)
    model = Model(parser, textFilter, imageFilter, config.eventFiles)
    LifeHistory = LifeHistoryApp(0, model)
    t = RescanningThread(config.imageFolders, parser, SimpleDateReader(), LifeHistory)
    t.start_if_needed()    
    LifeHistory.MainLoop()



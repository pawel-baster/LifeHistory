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
    parser = TextFileParser(config.eventFiles)
    textFilter = GetClosestEventsFilter(config.minNumberOfEvents)
    imageFilter = SimpleEventFilter()
    model = Model(parser, textFilter, imageFilter)
    #app = wx.PySimpleApp(0)
    #wx.InitAllImageHandlers()
    #frame_1 = LifeHistoryMainFrame(model, None, -1, "")
    ##app.SetTopWindow(frame_1)
    #frame_1.Show()
    #app.MainLoop()
    LifeHistory = LifeHistoryApp(0, model)
    LifeHistory.MainLoop()




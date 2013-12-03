import wx

class BackgroundAppIcon(wx.TaskBarIcon):

    TBMENU_CLOSE   = wx.NewId()

    def __init__(self, frame, icon, tooltip):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
 
        # Set the image
        self.tbIcon = icon
 
        self.SetIcon(self.tbIcon, tooltip)
 
        # bind some events
        self.Bind(wx.EVT_MENU, self.onTaskBarClose, id=self.TBMENU_CLOSE)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.onToggleVisibility)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.onTaskBarLeftClick)
 
    def createPopupMenu(self, evt=None):
        """
        This method is called by the base class when it needs to popup
        the menu for the default EVT_RIGHT_DOWN event.  Just create
        the menu how you want it and return it from this function,
        the base class takes care of the rest.
        """
        menu = wx.Menu()
        menu.Append(self.TBMENU_CLOSE,   "Exit Program")
        return menu
 
    def onToggleVisibility(self, evt):
        """
        Show or hide on left click on the tray icon
        """
        if self.frame.IsShown():
            self.frame.Hide()
        else:
            self.frame.Show()
            self.normal()
 
    def onTaskBarClose(self, evt):
        """
        Destroy the taskbar icon and frame from the taskbar icon itself
        """
        self.frame.exit()
 
    def onTaskBarLeftClick(self, evt):
        """
        Create the right-click menu
        """
        menu = self.createPopupMenu()
        self.PopupMenu(menu)
        menu.Destroy()

class TwoStateBackgroundAppIcon (BackgroundAppIcon):
    
    def __init__(self, frame, standard_icon, highlighted_icon, tooltip):
        BackgroundAppIcon.__init__(self, frame, standard_icon, tooltip)
        self.standard_icon = standard_icon
        self.highlighted_icon = highlighted_icon

    def highlight(self):
        self.SetIcon(self.highlighted_icon)

    def normal(self):
        self.SetIcon(self.standard_icon)

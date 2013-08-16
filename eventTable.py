import wx.grid

class EventTable(wx.grid.PyGridTableBase):
  
    def GetNumberRows(self):
        """Return the number of rows in the grid"""
        return len(self.events)

    def GetNumberCols(self):
        """Return the number of columns in the grid"""
        return 2

    def IsEmptyCell(self, row, col):
        """Return True if the cell is empty"""
        return False

    def GetTypeName(self, row, col):
        """Return the name of the data type of the value in the cell"""
        return None

    def GetValue(self, row, col):
        """Return the value of a cell"""
        if col == 0:
            return str(self.events[row].startDate)
        else: 
            return self.events[row].content

    def SetValue(self, row, col, value):
        """Set the value of a cell"""
        pass
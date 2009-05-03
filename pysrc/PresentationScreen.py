import wx
import config as cfg
from MyImage import *

class PresentationScreen(wx.Frame):
    def __init__(self, displayindex = 0):
        geometry = wx.Display(displayindex).GetGeometry()
        position = (geometry[0], geometry[1])
        self.size = (geometry[2], geometry[3])
        style = wx.NO_BORDER | wx.STAY_ON_TOP
        super(PresentationScreen, self).__init__(None, wx.ID_ANY, cfg.title,
                                                 style = style,
                                                 pos = position,
                                                 size = self.size)
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.static_bitmap = wx.StaticBitmap(self, wx.ID_ANY)
        box.Add(self.static_bitmap, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(box)
        self.panel = wx.Panel(self, wx.ID_ANY, size = (0, 0), pos = (0, 0))
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0))

    def load(self, slideindex):
        bitmap = cfg.slidelist[slideindex].scaleImageToBitmap(self.size)
        self.static_bitmap.SetBitmap(bitmap)
        self.Layout()


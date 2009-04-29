import wx
import config as cfg
from scaleImage import scaleImage

class PresentorsScreen(wx.Frame):
    def __init__(self, displayindex = 0):
        geometry = wx.Display(displayindex).GetGeometry()
        position = (geometry[0], geometry[1])
        self.size = (geometry[2], geometry[3])
        style = wx.NO_BORDER | wx.STAY_ON_TOP
        super(PresentorsScreen, self).__init__(None, wx.ID_ANY, cfg.title,
                                               style = style,
                                               size = self.size,
                                               pos = position)
        self.SetBackgroundColour(wx.Colour(80, 80, 80))
        self.static_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY)
        self.static_bitmap2 = wx.StaticBitmap(self, wx.ID_ANY)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.static_bitmap1, 99, wx.ALIGN_CENTER_VERTICAL)
        hbox.AddStretchSpacer(2)
        hbox.Add(self.static_bitmap2, 99, wx.ALIGN_CENTER_VERTICAL)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(hbox, 179, wx.ALIGN_CENTER_HORIZONTAL)
        box.AddStretchSpacer(1)
        font = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        textcolor = wx.Colour(210, 210 , 210)
        self.clock = wx.StaticText(self, wx.ID_ANY, "13:37:00")
        self.clock.SetForegroundColour(textcolor)
        self.clock.SetFont(font)
        hbox2.Add(self.clock , 2, wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddStretchSpacer(1)
        self.countDown = wx.StaticText(self, wx.ID_ANY, "10.00")
        self.countDown.SetForegroundColour(textcolor)
        self.countDown.SetFont(font)
        hbox2.Add(self.countDown , 2, wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddStretchSpacer(1)
        self.countUp = wx.StaticText(self, wx.ID_ANY, "00:00")
        self.countUp.SetForegroundColour(textcolor)
        self.countUp.SetFont(font)
        hbox2.Add(self.countUp , 2, wx.ALIGN_CENTER_VERTICAL)
        box.Add(hbox2, 17, wx.ALIGN_CENTER_HORIZONTAL)

        self.panel = wx.Panel(self, wx.ID_ANY)
        box.Add(self.panel, 3, wx.EXPAND)

        self.SetSizer(box)

    def load(self, slideindex):
        method = "scale"
        if (self.size[0] < 1024) or (self.size[1] < 768):
            method = "stretch"

        width = int(float(self.size[0]) / 200 * 99)
        height = int(float(self.size[1]) / 200 * 179)
        bitmap1 = scaleImage(cfg.slidelist[slideindex],
                             (width, height),
                             method = method)
        bitmap2 = scaleImage(cfg.slidelist[slideindex + 1],
                             (width, height),
                             method = method)
        self.static_bitmap1.SetBitmap(bitmap1)
        self.static_bitmap2.SetBitmap(bitmap2)
        self.Layout()


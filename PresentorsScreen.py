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
        self.hbox = wx.GridSizer(1, 2, 5, 5)
        self.hbox.Add(self.static_bitmap1, 99, wx.ALIGN_CENTER_VERTICAL)
        self.hbox.Add(self.static_bitmap2, 99, wx.ALIGN_CENTER_VERTICAL)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.hbox, 179, wx.ALIGN_CENTER_HORIZONTAL)
        self.box.AddStretchSpacer(1)
        font = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        textcolor = wx.Colour(210, 210 , 210)
        self.clock = wx.StaticText(self, wx.ID_ANY, "13:37:00")
        self.clock.SetForegroundColour(textcolor)
        self.clock.SetFont(font)
        hbox2.Add(self.clock , 3, wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddStretchSpacer(1)
        self.countDown = wx.StaticText(self, wx.ID_ANY, "10.00")
        self.countDown.SetForegroundColour(textcolor)
        self.countDown.SetFont(font)
        hbox2.Add(self.countDown , 3, wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddStretchSpacer(1)
        self.countUp = wx.StaticText(self, wx.ID_ANY, "00:00")
        self.countUp.SetForegroundColour(textcolor)
        self.countUp.SetFont(font)
        hbox2.Add(self.countUp , 3, wx.ALIGN_CENTER_VERTICAL)
        self.box.Add(hbox2, 17, wx.ALIGN_CENTER_HORIZONTAL)

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.box.Add(self.panel, 3, wx.EXPAND)

        self.SetSizer(self.box)

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

    def index(self, slideindex):
        self.thumbs = []
        for i in xrange(slideindex - 4, slideindex + 4):
            self.thumbs.append(cfg.thumbnaillist[i])
        for i in xrange(9):
            bitmap = scaleImage(self.thumbs[i], (320, 240), method = "scale")
            self.static_thumbs[i].SetBitmap(bitmap)



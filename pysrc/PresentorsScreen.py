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
        self.SetBackgroundColour(cfg.presentorBackgroundColor)
        self.static_bitmap = []
        for i in xrange(9):
            self.static_bitmap.append(wx.StaticBitmap(self, wx.ID_ANY))
        self.hbox = wx.GridSizer(1, 2, 10, 10)
        self.hbox.Add(self.static_bitmap[0], 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.hbox.Add(self.static_bitmap[1], 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.hbox, 179, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
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
        self.Layout()

    def makeImageBorder(self, img, pixels = 5):
        img = img.Copy()
        color = cfg.presentorBorderColor
        size = img.GetSize()
        # top
        rect = wx.Rect(0, 0, size[0], pixels)
        img.SetRGBRect(rect, color[0], color[1], color[2])
        # left
        rect = wx.Rect(0, 0, pixels, size[1])
        img.SetRGBRect(rect, color[0], color[1], color[2])
        # bottom
        rect = wx.Rect(0, size[1] - pixels, size[0], size[1])
        img.SetRGBRect(rect, color[0], color[1], color[2])
        # right
        rect = wx.Rect(size[0] - pixels, 0, size[0], size[1])
        img.SetRGBRect(rect, color[0], color[1], color[2])
        return img


    def load(self, slideindex):
        method = "scale"
        if (self.size[0] < 1024) or (self.size[1] < 768):
            method = "stretch"

        width = int(float(self.size[0]) / 2) - 5
        height = int(float(self.size[1]) / 200 * 179)
        if cfg.index:
            self.hbox.SetRows(3)
            self.hbox.SetCols(3)
            width = int(float(self.size[0]) / 3) - 5
            height = int(float(height) / 3)
            for i in xrange(9):
                img = cfg.thumbnaillist[slideindex + i - 4]
                if i == 4:
                    img = self.makeImageBorder(img)
                bitmap = scaleImage(img, (width, height), method = "scale")
                self.static_bitmap[i].SetBitmap(bitmap)
        else:
            self.hbox.SetRows(1)
            self.hbox.SetCols(2)
            bitmap1 = scaleImage(cfg.slidelist[slideindex],
                                 (width, height),
                                 method = method)
            bitmap2 = scaleImage(cfg.slidelist[slideindex + 1],
                                 (width, height),
                                 method = method)
            self.static_bitmap[0].SetBitmap(bitmap1)
            self.static_bitmap[1].SetBitmap(bitmap2)
        self.Layout()

    def index(self, slideindex):
        if cfg.index:
            for i in xrange(2, 9):
                self.static_bitmap[i].Show()
                self.hbox.Add(self.static_bitmap[i], 0, wx.ALIGN_CENTER_HORIZONTAL)
            self.thumbs = []
            for i in xrange(slideindex - 4, slideindex + 5):
                self.thumbs.append(cfg.thumbnaillist[i])
            self.load(slideindex)
        else:
            for i in xrange(2, 9):
                self.static_bitmap[i].Hide()
                self.hbox.Detach(self.static_bitmap[i])
            self.load(slideindex)



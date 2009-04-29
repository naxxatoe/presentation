import wx
import config as cfg

class NumberFrame(wx.Frame):
    def __init__(self, displayindex):
        geometry = wx.Display(displayindex).GetGeometry()
        style = wx.NO_BORDER | wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW
        super(NumberFrame, self).__init__(None, wx.ID_ANY, cfg.title,
                                          style = style)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        box = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(cfg.numberFontSize, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        text = wx.StaticText(self, wx.ID_ANY, str(displayindex))
        text.SetFont(font)
        box.Add(text, 0, wx.ALIGN_CENTER)
        self.SetSizerAndFit(box)
        size = self.GetSize()
        position = (geometry[0] + (geometry[2] / 2) - (size[0] / 2),
                    geometry[1] + (geometry[3] / 2) - (size[1] / 2))
        self.SetPosition(position)
        self.Show()


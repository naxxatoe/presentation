import wx
import config as cfg

class DisplayChoice(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        super(DisplayChoice, self).__init__(None, wx.ID_ANY, cfg.title,
                                            style = style)
        self.choices = ["-- Nothing --", "Audience", "Presentor"]
        displays = wx.Display.GetCount()
        box = wx.BoxSizer(wx.VERTICAL)
        self.selections = []
        for d in xrange(displays):
            choice = wx.Choice(self, wx.ID_ANY, choices = self.choices)
            choice.SetSelection(0)
            self.selections.append(choice)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(wx.StaticText(self, wx.ID_ANY,
                                   "Display " + str(d) + ": "),
                     0, wx.ALIGN_CENTER_VERTICAL)
            hbox.Add(choice, 0, wx.ALIGN_CENTER_VERTICAL)
            box.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.spinctrl = wx.SpinCtrl(self, wx.ID_ANY,
                                    min = 1,
                                    max = 120,
                                    initial = 20)
        box.Add(self.spinctrl, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.button = wx.Button(self, wx.ID_ANY, label = "OK")
        box.Add(self.button, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizerAndFit(box)
        self.Show()


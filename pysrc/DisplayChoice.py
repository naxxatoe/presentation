# DouF00 - fat free presentations
# Copyright (C) 2009  Martin Ptacek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        timelabel = wx.StaticText(self, wx.ID_ANY, "Time:")
        hbox.Add(timelabel, 0, wx.ALIGN_CENTER_VERTICAL)
        self.spinctrl = wx.SpinCtrl(self, wx.ID_ANY,
                                    min = 1,
                                    max = 120,
                                    initial = 20)
        hbox.Add(self.spinctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        box.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.button = wx.Button(self, wx.ID_ANY, label = "OK")
        box.Add(self.button, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizerAndFit(box)
        self.Show()


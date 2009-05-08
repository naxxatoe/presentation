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


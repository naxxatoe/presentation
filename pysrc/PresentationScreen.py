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
from MyImage import *

class PresentationScreen(wx.Frame):
    def __init__(self, displayindex = 0):
        self.displayindex = displayindex
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


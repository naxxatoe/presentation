# DouF00 - fat free presentations
# Copyright (C) 2009  Martin Ptacek
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author: natano (Martin Ptacek)
# Author: naxxatoe (Sebastian Maier)
# Email: natanoptacek@gmail.com
# Web: http://nicenamecrew.com/

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


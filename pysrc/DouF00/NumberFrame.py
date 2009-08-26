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
# Email: natanoptacek@gmail.com
# Web: http://nicenamecrew.com/

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


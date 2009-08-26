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
from MyImage import *

class PresentorsScreen(wx.Frame):
    def __init__(self, displayindex = 0):
        self.displayindex = displayindex
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
        self.countDown = wx.StaticText(self, wx.ID_ANY, "  10.00  ")
        self.countDown.SetForegroundColour(textcolor)
        self.countDown.SetFont(font)
        hbox2.Add(self.countDown , 3, wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddStretchSpacer(1)
        self.countUp = wx.StaticText(self, wx.ID_ANY, "  00:00  ")
        self.countUp.SetForegroundColour(textcolor)
        self.countUp.SetFont(font)
        hbox2.Add(self.countUp , 3, wx.ALIGN_CENTER_VERTICAL)
        self.box.Add(hbox2, 17, wx.ALIGN_CENTER_HORIZONTAL)
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.box.Add(self.panel, 3, wx.EXPAND)
        self.SetSizer(self.box)
        self.numbers = []

        textcolor = wx.Colour(210, 210 , 210)
        font = wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        for i in xrange(9):
            self.numbers.append(wx.StaticText(self, wx.ID_ANY, "0"))
            self.numbers[i].Hide()
            self.numbers[i].SetForegroundColour(textcolor)
            self.numbers[i].SetFont(font)

        self.Layout()

    def load(self, slideindex, prevSlide = None):
        method = "scale"
        if (self.size[0] < 1024) or (self.size[1] < 768):
            method = "stretch"

        width = int(float(self.size[0]) / 2) - 5
        height = int(float(self.size[1]) / 200 * 179)
        update = (prevSlide != None) and ((prevSlide - ((prevSlide + 1) % 9)) ==
                                          (slideindex - ((slideindex + 1) % 9)))
        if cfg.index:
            self.hbox.SetRows(3)
            self.hbox.SetCols(3)
            width = int(float(self.size[0]) / 3) - 5
            height = int(float(height) / 3)
            if update:
                updateList = [(slideindex + 1) % 9, (prevSlide + 1) % 9]
            else:
                updateList = xrange(9)

            for i in updateList:
                slidelistindex = slideindex - ((slideindex + 1) % 9) + i
                img = cfg.thumbnaillist[slidelistindex]
                if i == (slideindex + 1) % 9:
                    img = img.makeImageBorder()

                bitmap = img.scaleImageToBitmap((width, height), method = "stretch")
                self.static_bitmap[i].SetBitmap(bitmap)

            if not update:
                self.Layout()

            for i in updateList:
                slidelistindex = slideindex - ((slideindex + 1) % 9) + i
                self.numbers[i].SetLabel(str(slidelistindex + 1))

            self.Layout()
            for i in updateList:
                pos = self.static_bitmap[i].GetPosition()
                x = pos[0] + self.static_bitmap[i].GetSize()[0] - self.numbers[i].GetSize()[0] - 5
                y = pos[1] + 5
                self.numbers[i].SetPosition((x, y))

        else:
            self.hbox.SetRows(1)
            self.hbox.SetCols(2)
            image1 = cfg.slidelist[slideindex]
            image1 = image1.makeImageBorder()
            bitmap1 = image1.scaleImageToBitmap((width, height),
                                                method = method)
            bitmap2 = cfg.slidelist[slideindex + 1].scaleImageToBitmap(
                                                        (width, height),
                                                        method = method)
            self.static_bitmap[0].SetBitmap(bitmap1)
            self.static_bitmap[1].SetBitmap(bitmap2)

        self.Layout()
        if not update:
            self.Refresh()

    def index(self, slideindex, force = False):
        if force == True:
            cfg.index = False
        if cfg.index:
            for i in xrange(2, 9):
                self.static_bitmap[i].Show()
                self.hbox.Add(self.static_bitmap[i], 0, wx.ALIGN_CENTER_HORIZONTAL)

            self.thumbs = []
            for i in xrange(slideindex - 4, slideindex + 5):
                self.thumbs.append(cfg.thumbnaillist[i])

            for i in xrange(9):
                self.numbers[i].Show()

            self.load(slideindex)

        else:
            for i in xrange(2, 9):
                self.static_bitmap[i].Hide()
                self.hbox.Detach(self.static_bitmap[i])

            for i in xrange(9):
                self.numbers[i].Hide()

            self.load(slideindex)



# $Id: PresentorsScreen.py,v 1.5 2011-02-20 01:38:12 natano Exp $
# 
# Copyright (c) 2010 Martin Natano <natano@natano.net>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import wx

from DouF00 import appcfg

class PresentorsScreen(wx.Frame):
    def __init__(self, displayindex = 0):
        self.displayindex = displayindex
        geometry = wx.Display(displayindex).GetGeometry()
        position = (geometry[0], geometry[1])
        self.size = (geometry[2], geometry[3])
        style = wx.NO_BORDER | wx.STAY_ON_TOP
        super(PresentorsScreen, self).__init__(None, wx.ID_ANY, appcfg.title,
            style = style, size = self.size, pos = position)
        self.SetBackgroundColour(appcfg.presentorBackgroundColor)
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
        self.clock = wx.StaticText(self, wx.ID_ANY, '13:37:00')
        self.clock.SetForegroundColour(textcolor)
        self.clock.SetFont(font)
        hbox2.Add(self.clock , 3, wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddStretchSpacer(1)
        self.countDown = wx.StaticText(self, wx.ID_ANY, '  10.00  ')
        self.countDown.SetForegroundColour(textcolor)
        self.countDown.SetFont(font)
        hbox2.Add(self.countDown , 3, wx.ALIGN_CENTER_VERTICAL)
        hbox2.AddStretchSpacer(1)
        self.countUp = wx.StaticText(self, wx.ID_ANY, '  00:00  ')
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
            self.numbers.append(wx.StaticText(self, wx.ID_ANY, '0'))
            self.numbers[i].Hide()
            self.numbers[i].SetForegroundColour(textcolor)
            self.numbers[i].SetFont(font)

        self.Layout()

    def load(self, slideindex, prevSlide = None):
        method = 'scale'
        if self.size[0] < 1024 or self.size[1] < 768:
            method = 'stretch'

        width = int(float(self.size[0]) / 2) - 5
        height = int(float(self.size[1]) / 200 * 179)
        update = prevSlide != None and (
            prevSlide - ((prevSlide + 1) % 9) ==
            slideindex - ((slideindex + 1) % 9))

        if appcfg.index:
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
                img = appcfg.thumbnaillist[slidelistindex]
                if i == (slideindex + 1) % 9:
                    img = img.makeImageBorder(appcfg.presentorBorderColor)

                bitmap = img.scaleImageToBitmap((width, height),
                    method=method)
                self.static_bitmap[i].SetBitmap(bitmap)

            if not update:
                self.Layout()

            for i in updateList:
                slidelistindex = slideindex - ((slideindex + 1) % 9) + i
                self.numbers[i].SetLabel(str(slidelistindex + 1))

            self.Layout()
            for i in updateList:
                pos = self.static_bitmap[i].GetPosition()
                x = pos[0] + self.static_bitmap[i].GetSize()[0] - \
                    self.numbers[i].GetSize()[0] - 5
                y = pos[1] + 5
                self.numbers[i].SetPosition((x, y))

        else:
            self.hbox.SetRows(1)
            self.hbox.SetCols(2)
            image1 = appcfg.slidelist[slideindex]
            image1 = image1.makeImageBorder(appcfg.presentorBorderColor)
            bitmap1 = image1.scaleImageToBitmap((width, height),
                method = method)
            bitmap2 = appcfg.slidelist[slideindex + 1].scaleImageToBitmap(
                (width, height), method = method)
            self.static_bitmap[0].SetBitmap(bitmap1)
            self.static_bitmap[1].SetBitmap(bitmap2)

        self.Layout()
        if not update:
            self.Refresh()

    def index(self, slideindex, force = False):
        if force == True:
            appcfg.index = False
        if appcfg.index:
            for i in xrange(2, 9):
                self.static_bitmap[i].Show()
                self.hbox.Add(self.static_bitmap[i], 0,
                    wx.ALIGN_CENTER_HORIZONTAL)

            self.thumbs = []
            for i in xrange(slideindex - 4, slideindex + 5):
                self.thumbs.append(appcfg.thumbnaillist[i])

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



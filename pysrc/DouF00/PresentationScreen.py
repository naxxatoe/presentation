# $Id: PresentationScreen.py,v 1.4 2011-02-20 01:38:12 natano Exp $
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

class PresentationScreen(wx.Frame):
    def __init__(self, displayindex = 0):
        self.displayindex = displayindex
        geometry = wx.Display(displayindex).GetGeometry()
        position = (geometry[0], geometry[1])
        self.size = (geometry[2], geometry[3])
        style = wx.NO_BORDER | wx.STAY_ON_TOP
        super(PresentationScreen, self).__init__(None, wx.ID_ANY,
            appcfg.title, style = style, pos = position, size = self.size)
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.static_bitmap = wx.StaticBitmap(self, wx.ID_ANY)
        box.Add(self.static_bitmap, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(box)
        self.panel = wx.Panel(self, wx.ID_ANY, size = (0, 0), pos = (0, 0))
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0))

    def load(self, slideindex):
        bitmap = appcfg.slidelist[slideindex].scaleImageToBitmap(self.size)
        self.static_bitmap.SetBitmap(bitmap)
        self.Layout()


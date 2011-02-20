# $Id: NumberFrame.py,v 1.4 2011-02-20 01:38:12 natano Exp $
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

class NumberFrame(wx.Frame):
    def __init__(self, displayindex):
        geometry = wx.Display(displayindex).GetGeometry()
        style = wx.NO_BORDER | wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW
        super(NumberFrame, self).__init__(None, wx.ID_ANY, appcfg.title,
            style = style)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        box = wx.BoxSizer(wx.VERTICAL)
        font = wx.Font(appcfg.numberFontSize, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        text = wx.StaticText(self, wx.ID_ANY, str(displayindex))
        text.SetFont(font)
        box.Add(text, 0, wx.ALIGN_CENTER)
        self.SetSizerAndFit(box)
        size = self.GetSize()
        position = (geometry[0] + (geometry[2] / 2) - (size[0] / 2),
                    geometry[1] + (geometry[3] / 2) - (size[1] / 2))
        self.SetPosition(position)
        self.Show()


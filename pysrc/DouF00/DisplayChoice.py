# $Id: DisplayChoice.py,v 1.5 2011-02-20 01:38:12 natano Exp $
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
from DouF00.usercfg import config

class DisplayChoice(wx.Frame):
    def __init__(self):
        geometry = wx.Display(0).GetGeometry()
        style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        super(DisplayChoice, self).__init__(None, wx.ID_ANY, appcfg.title,
            style = style)
        self.choices = ['-- Nothing --', 'Audience', 'Presentor']
        displays = wx.Display.GetCount()
        box = wx.BoxSizer(wx.VERTICAL)
        self.selections = []
        for d in xrange(displays):
            choice = wx.Choice(self, wx.ID_ANY, choices = self.choices)
            choice.SetSelection(2 if str(d) in config['presentor'] else 1)
            
            self.selections.append(choice)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(
                wx.StaticText(self, wx.ID_ANY, 'Display ' + str(d) + ': '),
                0, wx.ALIGN_CENTER_VERTICAL)
            hbox.Add(choice, 0, wx.ALIGN_CENTER_VERTICAL)
            box.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        timelabel = wx.StaticText(self, wx.ID_ANY, 'Time:')
        hbox.Add(timelabel, 0, wx.ALIGN_CENTER_VERTICAL)
        self.spinctrl = wx.SpinCtrl(self, wx.ID_ANY, min = 0, max = 120,
            initial = config['time'])
        hbox.Add(self.spinctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        box.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.button = wx.Button(self, wx.ID_ANY, label = 'OK')
        box.Add(self.button, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizerAndFit(box)
        position = (geometry[0] + 50, geometry[1] + 50)
        self.SetPosition(position)
        self.Show()


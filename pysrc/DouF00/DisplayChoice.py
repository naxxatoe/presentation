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
import appcfg
import usercfg

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
            choice.SetSelection(1)
            self.selections.append(choice)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(wx.StaticText(self, wx.ID_ANY,
                                   'Display ' + str(d) + ': '),
                     0, wx.ALIGN_CENTER_VERTICAL)
            hbox.Add(choice, 0, wx.ALIGN_CENTER_VERTICAL)
            box.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        timelabel = wx.StaticText(self, wx.ID_ANY, 'Time:')
        hbox.Add(timelabel, 0, wx.ALIGN_CENTER_VERTICAL)
        self.spinctrl = wx.SpinCtrl(self, wx.ID_ANY,
                                    min = 1,
                                    max = 120,
                                    initial = usercfg.config['time'])
        hbox.Add(self.spinctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        box.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.button = wx.Button(self, wx.ID_ANY, label = 'OK')
        box.Add(self.button, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizerAndFit(box)
        position = (geometry[0] + 50, geometry[1] + 50)
        self.SetPosition(position)
        self.Show()


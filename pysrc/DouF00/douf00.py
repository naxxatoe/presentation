#!/usr/bin/env python
# $Id: douf00.py,v 1.7 2011-02-20 01:38:12 natano Exp $
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

import os, sys, threading, time, atexit

import wx

from DouF00 import appcfg
from DouF00.PresentorsScreen import PresentorsScreen
from DouF00.PresentationScreen import PresentationScreen
from DouF00.NumberFrame import NumberFrame
from DouF00.DisplayChoice import DisplayChoice
from DouF00.ImageList import ImageList
from DouF00.usercfg import config
from DouF00.utils import *

class TriggerClock(wx.PyEvent):
    def __init__(self):
        super(TriggerClock, self).__init__()
        self.SetEventType(appcfg.EVT_CLOCK_ID)

class MyApp(wx.App):
    def OnInit(self):
        self.presentationScreens = []
        self.presentorsScreens = []
        atexit.register(self.exit)

        config.loadFile(appcfg.configFile)
        parser, args = config.loadArgv(sys.argv)

        self.preApp()
        atexit.register(self.postApp)

        if len(args) > 1:
            parser.error('Only one slidpath is supported.')
        elif len(args) == 1:
            slidepath = args[0]
        else:
            if config['slidepath']:
                slidepath = config['slidepath']
            else:
                slidepath = wx.FileSelector('Choose a file to open',
                    wildcard='*.pdf')
                if not slidepath:
                    print parser.format_help()
                    sys.exit('No path specified')

        slidetype = guessFiletype(slidepath)

        if not slidetype == 'PDF':
            if config['password']:
                parser.error('Option -S is only suitable for PDF files')
            if config['blankpage']:
                parser.error('Option -B is only supported with PDF files')

        if config['password']:
            appcfg.pdfpass = wx.GetPasswordFromUser('PDF password')

        if slidetype == 'dir':
            if config['blankslide']:
                config['blankslide'] = os.path.abspath(config['blankslide'])

            try:
                os.chdir(slidepath)
            except OSError:
                sys.exit('No such file or directory')

            appcfg.pictureFiles = []
            files = os.listdir(os.getcwd())

            # support for more picture types
            for fname in files:
                if guessFiletype(fname) in ('JPEG', 'PNG', 'BMP', 'PCX'):
                    appcfg.pictureFiles.append(fname)

            appcfg.pictureFiles.sort()

            if config['blankslide']:
                if guessFiletype(config['blankslide']) in ('JPEG', 'PNG',
                                                           'BMP', 'PCX'):
                    appcfg.blankslide = ('image', config['blankslide'])
                    if appcfg.blankslide[1] in appcfg.pictureFiles:
                        appcfg.pictureFiles.remove(appcfg.blankslide[1])
                else:
                    print('File type not supported')
                    sys.exit(1)

            else:
                appcfg.blankslide = ''

        elif slidetype == 'PDF':
            try:
                import poppler
            except ImportError:
                print 'python-poppler required'
                sys.exit(1)

            appcfg.pdfdoc = poppler.document_new_from_file(
                'file://{0}'.format(os.path.abspath(slidepath)),
                appcfg.pdfpass)
            appcfg.pictureFiles = []
            for i in xrange(appcfg.pdfdoc.get_n_pages()):
                appcfg.pictureFiles.append(i)

            if config['blankslide']:
                if guessFiletype(config['blankslide']) in ('JPEG', 'PNG',
                                                           'BMP', 'PCX'):
                    appcfg.blankslide = ('image', config['blankslide'])
                    if appcfg.blankslide[1] in appcfg.pictureFiles:
                        appcfg.pictureFiles.remove(appcfg.blankslide[1])
                else:
                    print('File type not supported')
                    sys.exit(1)

            elif not config['blankpage'] == 0:
                appcfg.blankslide = ('PDF', config['blankpage'] - 1)
                appcfg.pictureFiles.remove(appcfg.blankslide[1])

            else:
                appcfg.blankslide = ''

        elif slidetype == None:
            print('File type not supported')
            sys.exit(1)

        appcfg.thumbnaillist = ImageList('Thumbnails', appcfg.THUMBNAIL_SIZE)
        appcfg.slidelist = ImageList('Slides')

        displayCount = wx.Display.GetCount()
        self.numberFrames = []
        for d in xrange(displayCount):
            self.numberFrames.append(NumberFrame(d))

        self.choice = DisplayChoice()
        self.choice.button.Bind(wx.EVT_BUTTON, self.Run)
        self.runTime = 120
        self.startTime = int(time.mktime(time.localtime()))
        self.remainingTime = self.runTime
        self.elapsedTime = 0
        if config['autostart']:
            self.Run(None)

        return True

    def preApp(self):
        if config['predouf00']:
            os.system(config['predouf00'])

    def postApp(self):
        if config['postdouf00']:
            os.system(config['postdouf00'])

    def OnKeyPress(self, event):
        event.Skip()
        key = event.GetKeyCode()
        if key in (wx.WXK_RIGHT, wx.WXK_SPACE, wx.WXK_PAGEDOWN):
            self.NextSlide()
        elif key in (wx.WXK_LEFT, wx.WXK_PAGEUP):
            self.PrevSlide()
        elif key == wx.WXK_RETURN:
            self.exitIndex()
        elif key == wx.WXK_DOWN:
            if appcfg.index:
                self.NextSlide(3)
        elif key == wx.WXK_UP:
            if appcfg.index:
                self.PrevSlide(3)
        elif key in (ord('q'), ord('Q')):
            sys.exit()
        elif key in (ord('r'), ord('R')):
            self.startTime = int(time.time())
            self.elapsedTime = 0
        elif key in (ord('p'), ord('P')):
            appcfg.pause = not appcfg.pause
        elif key in (ord('s'), ord('S')):
            self.swapScreens()
        elif key in (ord('i'), ord('I'), wx.WXK_ESCAPE, wx.WXK_F5):
            if appcfg.index:
                for p in self.presentationScreens:
                    p.load(self.slideindex)
                    p.Show()
            appcfg.index = not appcfg.index
            for p in self.presentorsScreens:
                p.index(self.slideindex)

    def exit(self):
        allScreens = sum(
            [self.presentationScreens, self.presentorsScreens,], [])

        for p in allScreens:
            p.Destroy()

    def swapScreens(self):
        presentationScreens = []
        presentorsScreens = []
        for i in xrange(len(self.presentationScreens)):
            displayindex = self.presentationScreens[i].displayindex
            self.presentationScreens[i].Destroy()
            p = PresentorsScreen(displayindex)
            p.load(self.slideindex)
            p.Show()
            presentorsScreens.append(p)

        for i in xrange(len(self.presentorsScreens)):
            displayindex = self.presentorsScreens[i].displayindex
            self.presentorsScreens[i].index(self.slideindex, force = True)
            self.presentorsScreens[i].Destroy()
            p = PresentationScreen(displayindex)
            p.load(self.slideindex)
            p.Show()
            presentationScreens.append(p)

        self.presentationScreens = presentationScreens
        self.presentorsScreens = presentorsScreens
        for p in self.presentationScreens:
            p.load(self.slideindex)
            p.Show()
            p.panel.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
            for thing in (p, p.panel, p.static_bitmap):
                thing.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
                thing.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

            p.panel.SetFocus()

        for p in self.presentorsScreens:
            p.load(self.slideindex)
            p.Show()
            p.panel.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
            for thing in (p, p.panel, p.clock, p.countUp, p.countDown, 
                          p.static_bitmap[0], p.static_bitmap[1]):
                thing.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
                thing.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

            p.panel.SetFocus()

    def OnLeftClick(self, event):
        event.Skip()
        self.NextSlide()

    def OnRightClick(self, event):
        event.Skip()
        self.PrevSlide()

    def exitIndex(self):
        if appcfg.index:
            appcfg.index = not appcfg.index
            for p in self.presentorsScreens:
                p.index(self.slideindex)
            for p in self.presentationScreens:
                p.load(self.slideindex)
                p.Show()

    def Run(self, event):
        self.runTime = self.choice.spinctrl.GetValue() * 60
        self.slideindex = -1
        displayCount = wx.Display.GetCount()
        for displayindex in xrange(displayCount):
            selection = self.choice.choices[
                self.choice.selections[displayindex].GetSelection()]
            if selection == 'Audience':
                self.presentationScreens.append(
                    PresentationScreen(displayindex = displayindex))
            elif selection == 'Presentor':
                self.presentorsScreens.append(
                    PresentorsScreen(displayindex = displayindex))

        self.choice.Destroy()
        for numberFrame in self.numberFrames:
            numberFrame.Destroy()
        
        if not self.presentationScreens and not self.presentorsScreens:
            sys.exit()

        for p in self.presentationScreens:
            p.load(self.slideindex)
            p.Show()
            p.panel.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
            for thing in (p, p.panel, p.static_bitmap):
                thing.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
                thing.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

            p.panel.SetFocus()

        for p in self.presentorsScreens:
            p.load(self.slideindex)
            p.Show()
            p.panel.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
            for thing in (p, p.panel, p.clock, p.countUp, p.countDown,
                          p.static_bitmap[0], p.static_bitmap[1]):
                thing.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
                thing.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

            p.panel.SetFocus()

        self.setClock('f00')
        t = self.Clock(self, self.presentorsScreens)
        t.setDaemon(True)
        t.start()
        self.Connect(-1, -1, appcfg.EVT_CLOCK_ID, self.setClock)

    def setClock(self, event):
        t = time.localtime()
        now = int(time.time())
        is_running = 0
        if ((0 <= self.slideindex < len(appcfg.pictureFiles)) and \
            self.remainingTime > 0) and not appcfg.pause:
            is_running = 1
        else:
            self.startTime = now - self.elapsedTime

        if is_running == 1:
            self.elapsedTime = now - self.startTime + 1
        else:
            self.elapsedTime = now - self.startTime

        self.remainingTime = self.runTime - self.elapsedTime
        for s in self.presentorsScreens:
            tstr = '{0:02}:{1:02}:{2:02}'.format(t[3], t[4], t[5])
            s.clock.SetLabel(tstr)
            countUpStr = '  {0:02}:{1:02}  '.format(
                self.elapsedTime / 60, self.elapsedTime % 60)
            countDownStr = '  {0:02}:{1:02}  '.format(
                self.remainingTime / 60, self.remainingTime % 60)
            s.countUp.SetLabel(countUpStr)
            s.countDown.SetLabel(countDownStr)
            try:
                red = int(float(255) * self.elapsedTime / self.runTime)
                green = int(float(150) * self.remainingTime / self.runTime)
                color = wx.Colour(red, green, 0)
                s.panel.SetBackgroundColour(color)
                if self.remainingTime < 120:
                    color = wx.Colour(255, 0, 0)
                    s.countDown.SetForegroundColour(color)
            except:
                pass

    class Clock(threading.Thread):
        def __init__(self, mainApp, presentorsScreens):
            self.mainApp = mainApp 
            self.presentorsScreens = presentorsScreens
            super(MyApp.Clock, self).__init__()
        def run(self):
            while 1:
                wx.PostEvent(self.mainApp, TriggerClock())
                time.sleep(1)


    def NextSlide(self, step = 1):
        if (self.slideindex + step > len(appcfg.pictureFiles)) and \
            config['exitafterlastslide'] and not appcfg.index:
            sys.exit()

        if self.slideindex + step <= len(appcfg.pictureFiles):
            self.slideindex += step

        if not appcfg.index:
            for p in self.presentationScreens:
                p.load(self.slideindex)
                p.Show()

        for p in self.presentorsScreens:
            p.load(self.slideindex, prevSlide = self.slideindex - step)
            p.Show()
         
    def PrevSlide(self, step = 1):
        if self.slideindex - step >= -1:
            self.slideindex -= step

        if not appcfg.index:
            for p in self.presentationScreens:
                p.load(self.slideindex)
                p.Show()

        for p in self.presentorsScreens:
            p.load(self.slideindex, prevSlide = self.slideindex + step)
            p.Show()
         

def main():
    app = MyApp()
    app.MainLoop()

if __name__ == '__main__': main()


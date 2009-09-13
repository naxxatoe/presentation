#!/usr/bin/env python
#
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
# THE SOFTWARE..
#
# Author: natano (Martin Ptacek)
# Author: naxxatoe (Sebastian Maier)
# Email: natanoptacek@gmail.com
# Web: http://nicenamecrew.com/

import os
import sys
import threading
import time

WXVER_REQ = '2.8'
if 'wx' not in sys.modules and 'wxPython' not in sys.modules:
    import wxversion
    wxversion.ensureMinimal(WXVER_REQ)

try:
    import wx
    assert wx.VERSION_STRING >= WXVER_REQ
except:
    print('wxpython >= %s required!' % WXVER_REQ)
    sys.exit(1)


import appcfg
from PresentorsScreen import PresentorsScreen
from PresentationScreen import PresentationScreen
from SlideList import SlideList
from NumberFrame import NumberFrame
from DisplayChoice import DisplayChoice
from ThumbnailList import ThumbnailList
import atexit
import usercfg

def printUsage():
    print('Usage: %s [path]' % os.path.basename(sys.argv[0]))

class TriggerClock(wx.PyEvent):
    def __init__(self):
        super(TriggerClock, self).__init__()
        self.SetEventType(appcfg.EVT_CLOCK_ID)

def filetype(path):
    if os.path.isdir(path):
        return 'dir'

    file = open(path, 'r')
    filemagic = file.read(8)
    file.close()
    for type, magic in appcfg.filetypes:
        if magic == filemagic[:len(magic)]:
            return type

    return None

class MyApp(wx.App):
    def OnInit(self):
        print(appcfg.title + ' ' + appcfg.__version__)

        self.presentationScreens = []
        self.presentorsScreens = []
        atexit.register(self.exit)

        usercfg.parseConfig()
        self.preApp()
        atexit.register(self.postApp)


        try:
            slidepath = sys.argv[1]
        except IndexError:
            dirdialog = wx.DirDialog(None)
            if (dirdialog.ShowModal() == wx.ID_OK):
                slidepath = dirdialog.GetPath()
            else:
                printUsage()
                sys.exit('No path specified')

        slidetype = filetype(slidepath)
        if slidetype == 'dir':
            try:
                os.chdir(slidepath)
            except OSError:
                sys.exit('No such file or directory')

            appcfg.pictureFiles = []
            files = os.listdir(os.getcwd())

            # support for more picture types
            for file in files:
                if filetype(file) in ('JPEG', 'PNG', 'BMP', 'PCX'):
                    appcfg.pictureFiles.append(file)

            appcfg.pictureFiles.sort()

            # DOC: if you place in your presentation directory a file with
            #      the name blank.foo where foo can be: jpeg,jpg,png,bmp or pcx
            #      that will be your first slide, your title slide, which
            #      shows up when you start douf00.
            #      It was chosen that way, because some people prefer it when they
            #      start the presentation to see a slide other don't prefer that
            #      so more freedom to the presentator to organize their presentation

            appcfg.blankslide = ''
            for type in ("jpg","jpeg","png","bmp","pcx"):
                if ('blank' + '.' + type) in appcfg.pictureFiles:
                    if filetype(file) in ('JPEG', 'PNG', 'BMP', 'PCX'):
                        appcfg.blankslide = ('blank' + '.' + type)
                        appcfg.pictureFiles.remove(appcfg.blankslide)
                        break

        elif slidetype == 'PDF':
            try:
                import poppler
            except ImportError:
                print 'python-poppler required!'
                sys.exit(1)

            appcfg.pdfdoc = poppler.document_new_from_file('file://%s' % os.path.abspath(slidepath), '')
            appcfg.pictureFiles = []
            for i in xrange(appcfg.pdfdoc.get_n_pages()):
                appcfg.pictureFiles.append(i)

            appcfg.blankslide = ''

        elif slidetype == None:
            print('Filetype not supported!')
            sys.exit(1)

        appcfg.thumbnaillist = ThumbnailList()
        appcfg.slidelist = SlideList()

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
        return True

    def preApp(self):
        if usercfg.config['preDouF00']:
            os.system(usercfg.config['preDouF00'])

    def postApp(self):
        if usercfg.config['postDouF00']:
            os.system(usercfg.config['postDouF00'])

    def OnKeyPress(self, event):
        event.Skip()
        key = event.GetKeyCode()
        if (key == wx.WXK_RIGHT) or (key == wx.WXK_SPACE) or (key == wx.WXK_PAGEDOWN):
            self.NextSlide()
        elif (key == wx.WXK_LEFT) or (key == wx.WXK_PAGEUP):
            self.PrevSlide()
        elif (key == wx.WXK_DOWN):
            if appcfg.index:
                self.NextSlide(3)
        elif (key == wx.WXK_UP):
            if appcfg.index:
                self.PrevSlide(3)
        elif (key == ord('q')) or (key == ord('Q')):
            sys.exit()
        elif (key == ord('r')) or (key == ord('R')):
            self.startTime = int(time.time())
            self.elapsedTime = 0
        elif (key == ord('p')) or (key == ord('P')):
            appcfg.pause = not appcfg.pause
        elif (key == ord('i')) or (key == ord('I')) or (key == wx.WXK_ESCAPE) or (key == wx.WXK_F5):
            if appcfg.index:
                for p in self.presentationScreens:
                    p.load(self.slideindex)
                    p.Show()
            appcfg.index = not appcfg.index
            for p in self.presentorsScreens:
                p.index(self.slideindex)
        elif (key == wx.WXK_RETURN):
            self.exitIndex()
        elif (key == ord('s')) or (key == ord('S')):
            self.swapScreens()

    def exit(self):
        for p in self.presentationScreens:
            p.Destroy()

        for p in self.presentorsScreens:
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
            for thing in (p, p.panel, p.clock, p.countUp, p.countDown, p.static_bitmap[0], p.static_bitmap[1]):
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
            if self.choice.choices[self.choice.selections[displayindex].GetSelection()] == 'Audience':
                self.presentationScreens.append(PresentationScreen(displayindex = displayindex))
            elif self.choice.choices[self.choice.selections[displayindex].GetSelection()] == 'Presentor':
                self.presentorsScreens.append(PresentorsScreen(displayindex = displayindex))

        self.choice.Destroy()
        for numberFrame in self.numberFrames:
            numberFrame.Destroy()
        
        if (self.presentationScreens == []) and (self.presentorsScreens == []):
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
            for thing in (p, p.panel, p.clock, p.countUp, p.countDown, p.static_bitmap[0], p.static_bitmap[1]):
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
            (self.remainingTime > 0)) and (not appcfg.pause):
            is_running = 1
        else:
            self.startTime = now - self.elapsedTime

        if is_running == 1:
            self.elapsedTime = now - self.startTime + 1
        else:
            self.elapsedTime = now - self.startTime

        self.remainingTime = self.runTime - self.elapsedTime
        for s in self.presentorsScreens:
            tstr = '%02d:%02d:%02d' % (t[3], t[4], t[5])
            s.clock.SetLabel(tstr)
            countUpStr = '  %02d:%02d  ' % (self.elapsedTime / 60,
                                        self.elapsedTime % 60)
            countDownStr = '  %02d:%02d  ' % (self.remainingTime / 60,
                                          self.remainingTime % 60)
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
        if (self.slideindex + step > len(appcfg.pictureFiles)) and usercfg.config['exitAfterLastSlide'] and not appcfg.index:
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


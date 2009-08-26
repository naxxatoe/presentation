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
import wx
#it would be more nice to print a useful message here....
assert wx.VERSION_STRING >= WXVER_REQ

import config as cfg
from PresentorsScreen import PresentorsScreen
from PresentationScreen import PresentationScreen
from SlideList import SlideList
from NumberFrame import NumberFrame
from DisplayChoice import DisplayChoice
from ThumbnailList import ThumbnailList
import atexit

def printUsage():
    print("Usage: " + sys.argv[0] + " [path]")

class TriggerClock(wx.PyEvent):
    def __init__(self):
        super(TriggerClock, self).__init__()
        self.SetEventType(cfg.EVT_CLOCK_ID)

def die():
    os.chdir(cfg.prevWD)

class MyApp(wx.App):
    def OnInit(self):
        print(cfg.title + " " + cfg.__version__)
        print("Copyright (C) 2009  " + cfg.__author__)
        print("This program comes with ABSOLUTELY NO WARRANTY.")
        print("This is free software, and you are welcome to redistribute it")
        print("and/or modify it under the terms of the MIT license.")

        atexit.register(die)
        try:
            basedir = sys.argv[1]
        except IndexError:
            dirdialog = wx.DirDialog(None)
            if (dirdialog.ShowModal() == wx.ID_OK):
                basedir = dirdialog.GetPath()
            else:
                printUsage()
                sys.exit("No path specified")

        self.td = None
        if basedir[-4:].lower() == ".pdf":
            import tempfile
            self.td = tempfile.mkdtemp(prefix="douf00")
            atexit.register(self.deleteTemp)
            os.system("gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=jpeg -r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dMaxStripSize=8192 -sOutputFile="+ os.path.join(self.td, "douf00_%04d.jpeg") + " " + basedir)

            basedir = self.td

        try:
            os.chdir(basedir)
        except OSError:
            sys.exit("No such file or directory")

        basedir = os.getcwd()

        cfg.pictureFiles = []
        files = os.listdir(basedir)
        for file in files:
            try:
                if (file[-4:].lower() == ".jpg") or (file[-5:].lower() == ".jpeg"):
                    cfg.pictureFiles.append(file)
            except IndexError:
                pass

        cfg.pictureFiles.sort()

        cfg.blankslide = ""
        if "blank.jpg" in cfg.pictureFiles:
            cfg.blankslide = "blank.jpg"
            cfg.pictureFiles.remove(cfg.blankslide)

        cfg.slidelist = SlideList()
        cfg.thumbnaillist = ThumbnailList()

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

    def deleteTemp(self):
        import shutil
        shutil.rmtree(self.td)

    def OnKeyPress(self, event):
        event.Skip()
        key = event.GetKeyCode()
        if (key == wx.WXK_RIGHT) or (key == wx.WXK_SPACE) or (key == wx.WXK_PAGEDOWN):
            self.NextSlide()
        elif (key == wx.WXK_LEFT) or (key == wx.WXK_PAGEUP):
            self.PrevSlide()
        elif (key == wx.WXK_DOWN):
            if cfg.index:
                self.NextSlide(3)
        elif (key == wx.WXK_UP):
            if cfg.index:
                self.PrevSlide(3)
        elif (key == ord('q')) or (key == ord('Q')):
            for p in self.presentationScreens:
                p.Destroy()

            for p in self.presentorsScreens:
                p.Destroy()

            sys.exit(0)
        elif (key == ord('r')) or (key == ord('R')):
            self.startTime = int(time.time())
            self.elapsedTime = 0
        elif (key == ord('p')) or (key == ord('P')):
            cfg.pause = not cfg.pause
        elif (key == ord('i')) or (key == ord('I')) or (key == wx.WXK_ESCAPE) or (key == wx.WXK_F5):
            if cfg.index:
                for p in self.presentationScreens:
                    p.load(self.slideindex)
                    p.Show()
            cfg.index = not cfg.index
            for p in self.presentorsScreens:
                p.index(self.slideindex)
        elif (key == wx.WXK_RETURN):
            if cfg.index:
                cfg.index = not cfg.index
                for p in self.presentorsScreens:
                    p.index(self.slideindex)
                for p in self.presentationScreens:
                    p.load(self.slideindex)
                    p.Show()
        elif (key == ord("s")) or (key == ord("S")):
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
                p.panel.SetFocus()

            for p in self.presentorsScreens:
                p.load(self.slideindex)
                p.Show()
                p.panel.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
                p.panel.SetFocus()


    def Run(self, event):
        self.runTime = self.choice.spinctrl.GetValue() * 60
        self.slideindex = -1
        displayCount = wx.Display.GetCount()
        self.presentationScreens = []
        self.presentorsScreens = []
        for displayindex in xrange(displayCount):
            if self.choice.choices[self.choice.selections[displayindex].GetSelection()] == "Audience":
                self.presentationScreens.append(PresentationScreen(displayindex = displayindex))
            elif self.choice.choices[self.choice.selections[displayindex].GetSelection()] == "Presentor":
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
            p.panel.SetFocus()

        for p in self.presentorsScreens:
            p.load(self.slideindex)
            p.Show()
            p.panel.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
            p.panel.SetFocus()

        self.setClock("f00")
        t = self.Clock(self, self.presentorsScreens)
        t.setDaemon(True)
        t.start()
        self.Connect(-1, -1, cfg.EVT_CLOCK_ID, self.setClock)

    def setClock(self, event):
        t = time.localtime()
        now = int(time.time())
        is_running = 0
        if ((0 <= self.slideindex < len(cfg.pictureFiles)) and \
            (self.remainingTime > 0)) and (not cfg.pause):
            is_running = 1
        else:
            self.startTime = now - self.elapsedTime

        if is_running == 1:
            self.elapsedTime = now - self.startTime + 1
        else:
            self.elapsedTime = now - self.startTime

        self.remainingTime = self.runTime - self.elapsedTime
        for s in self.presentorsScreens:
            tstr = "%02d:%02d:%02d" % (t[3], t[4], t[5])
            s.clock.SetLabel(tstr)
            countUpStr = "  %02d:%02d  " % (self.elapsedTime / 60,
                                        self.elapsedTime % 60)
            countDownStr = "  %02d:%02d  " % (self.remainingTime / 60,
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
        if self.slideindex + step <= len(cfg.pictureFiles):
            self.slideindex += step

        if not cfg.index:
            for p in self.presentationScreens:
                p.load(self.slideindex)
                p.Show()

        for p in self.presentorsScreens:
            p.load(self.slideindex, prevSlide = self.slideindex - step)
            p.Show()
         
    def PrevSlide(self, step = 1):
        if self.slideindex - step >= -1:
            self.slideindex -= step

        if not cfg.index:
            for p in self.presentationScreens:
                p.load(self.slideindex)
                p.Show()

        for p in self.presentorsScreens:
            p.load(self.slideindex, prevSlide = self.slideindex + step)
            p.Show()
         

def main():
    app = MyApp()
    app.MainLoop()

if __name__ == "__main__": main()

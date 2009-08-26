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
import config as cfg
import threading
import Queue

class SlideList(list):
    def __init__(self):
        super(SlideList, self).__init__()
        self.list = [None for i in xrange(len(cfg.pictureFiles))]
        self.queue = Queue.Queue()
        self.ParallelLoad(self.queue).start()

    def __getitem__(self, slideindex):
        if (slideindex < 0) or (slideindex >= len(self.list)):
            image = self.loadImage(slideindex)
        elif (self.list[slideindex] == None):
            self.list[slideindex] = self.loadImage(slideindex)
            image = self.list[slideindex]
        else:
            image = self.list[slideindex]

        self.queue.put(slideindex)

        return image

    def loadImage(self, slideindex):
        if (slideindex < 0) or (slideindex >= len(self.list)):
            if (slideindex > len(self.list)) or (cfg.blankslide == ""):
                buffer = "\0\0\0" * 320 * 240
                image = wx.ImageFromBuffer(320, 240, buffer)
            else:
                f = open(cfg.blankslide, "rb")
                image = wx.ImageFromStream(f)
                f.close()
        else:
            try:
                f = open(cfg.pictureFiles[slideindex], "rb")
                image = wx.ImageFromStream(f)
                f.close()
            except:
                print("Cant load image: ")

        return image

    class ParallelLoad(threading.Thread):
        def __init__(self, queue):
            self.queue = queue
            super(SlideList.ParallelLoad, self).__init__()
        def run(self):
            slideindex = self.queue.get()
            minIndex = slideindex - cfg.preLoadCache
            maxIndex = slideindex + cfg.preLoadCache
            if minIndex < 0:
                minIndex = 0

            if maxIndex > len(cfg.pictureFiles):
                maxIndex = len(cfg.pictureFiles)

            for i in xrange(minIndex, maxIndex):
                if cfg.slidelist[i] == None:
                    cfg.slidelist[i] = loadImage(i)

            for i in xrange(minIndex):
                cfg.slidelist[i] = None

            for i in xrange(maxIndex, len(cfg.slidelist)):
                cfg.slidelist[i] = None


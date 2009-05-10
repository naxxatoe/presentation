# DouF00 - fat free presentations
# Copyright (C) 2009  Martin Ptacek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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


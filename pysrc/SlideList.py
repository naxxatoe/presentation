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
                buffer = "\0\0\0"
                image = wx.ImageFromBuffer(1, 1, buffer)
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


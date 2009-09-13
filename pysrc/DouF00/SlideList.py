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
import threading
import Queue


class SlideList(list):
    def __init__(self):
        super(SlideList, self).__init__()
        self.list = [None for i in xrange(len(appcfg.pictureFiles))]
        self.blank = None
        if appcfg.pdfdoc:
            import sys
            slidecount = len(appcfg.pictureFiles)
            for i in xrange(len(appcfg.pictureFiles)):
                sys.stdout.write('\r* Loading Slides: %03d/%03d' % (i+1, slidecount))
                sys.stdout.flush()
                self.list[i] = self.loadImage(i)
            sys.stdout.write('\n')
        else:
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

        if not appcfg.pdfdoc:
            self.queue.put(slideindex)

        return image

    def loadImage(self, slideindex):
        if slideindex > len(self.list):
            buffer = '\0\0\0' * 320 * 240
            image = wx.ImageFromBuffer(320, 240, buffer)

        elif (slideindex < 0) or (slideindex == len(self.list)):
            if  not self.blank:
                if appcfg.blankslide == '':
                    buffer = '\0\0\0' * 320 * 240
                    image = wx.ImageFromBuffer(320, 240, buffer)
                else:
                    if appcfg.blankslide[0] == 'image':
                        f = open(appcfg.blankslide[1], 'rb')
                    elif appcfg.blankslide[0] == 'PDF':
                        import cairo
                        import cStringIO
                        page = appcfg.pdfdoc.get_page(appcfg.blankslide[1] - 1)
                        page_w, page_h = page.get_size()
                        img = cairo.ImageSurface(cairo.FORMAT_RGB24, 1024, 768)
                        context = cairo.Context(img)
                        context.scale(1024/page_w, 768/page_h)
                        context.set_source_rgb(1.0, 1.0, 1.0)
                        context.rectangle(0, 0, page_w, page_h)
                        context.fill()
                        page.render(context)
                        f = cStringIO.StringIO()
                        img.write_to_png(f)
                        f.seek(0)

                    self.blank = wx.ImageFromStream(f)
                    f.close()

            image = self.blank

        else:
            try:
                if appcfg.pdfdoc:
                    import cairo
                    import cStringIO
                    page = appcfg.pdfdoc.get_page(appcfg.pictureFiles[slideindex])
                    page_w, page_h = page.get_size()
                    img = cairo.ImageSurface(cairo.FORMAT_RGB24, 1024, 768)
                    context = cairo.Context(img)
                    context.scale(1024/page_w, 768/page_h)
                    context.set_source_rgb(1.0, 1.0, 1.0)
                    context.rectangle(0, 0, page_w, page_h)
                    context.fill()
                    page.render(context)
                    f = cStringIO.StringIO()
                    img.write_to_png(f)
                    f.seek(0)
                else:
                    f = open(appcfg.pictureFiles[slideindex], 'rb')

                image = wx.ImageFromStream(f)
                f.close()

            except:
                print('Cant load page: %s' % appcfg.pictureFiles[slideindex])

        return image

    class ParallelLoad(threading.Thread):
        def __init__(self, queue):
            self.queue = queue
            super(SlideList.ParallelLoad, self).__init__()
        def run(self):
            slideindex = self.queue.get()
            minIndex = slideindex - appcfg.preLoadCache
            maxIndex = slideindex + appcfg.preLoadCache
            if minIndex < 0:
                minIndex = 0

            if maxIndex > len(appcfg.pictureFiles):
                maxIndex = len(appcfg.pictureFiles)

            for i in xrange(minIndex, maxIndex):
                if appcfg.slidelist[i] == None:
                    appcfg.slidelist[i] = loadImage(i)

            for i in xrange(minIndex):
                appcfg.slidelist[i] = None

            for i in xrange(maxIndex, len(appcfg.slidelist)):
                appcfg.slidelist[i] = None


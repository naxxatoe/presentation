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
import threading
import config as cfg


class ThumbnailList(list):
    def __init__(self):
        if cfg.pdfdoc:
            import cairo
            import cStringIO
            import sys

        super(ThumbnailList, self).__init__()
        self.list = []
        slidecount = cfg.pdfdoc.get_n_pages()
        for filename in cfg.pictureFiles:
            if cfg.pdfdoc:
                sys.stdout.write('\r* Loading Thumbnails: %03d/%03d' % (filename+1, slidecount))
                sys.stdout.flush()
                page = cfg.pdfdoc.get_page(filename)
                page_w, page_h = page.get_size()
                img = cairo.ImageSurface(cairo.FORMAT_RGB24, 320, 240)
                context = cairo.Context(img)
                context.scale(320/page_w, 240/page_h)
                context.set_source_rgb(1.0, 1.0, 1.0)
                context.rectangle(0, 0, page_w, page_h)
                context.fill()
                page.render(context)
                f = cStringIO.StringIO()
                img.write_to_png(f)
                f.seek(0)
            else:
                f = open(filename, 'rb')

            image = wx.ImageFromStream(f)
            f.close()

            size = (320, 240)
            ImageSize = image.GetSize()
            ratioX = float(size[0]) / ImageSize[0]                                  
            ratioY = float(size[1]) / ImageSize[1]
            if ratioX < ratioY:
                ImageSize[0] = int(ImageSize[0] * ratioX)
                ImageSize[1] = int(ImageSize[1] * ratioX)
            else:
                ImageSize[0] = int(ImageSize[0] * ratioY)
                ImageSize[1] = int(ImageSize[1] * ratioY)

            image.Rescale(ImageSize[0], ImageSize[1])
            self.list.append(image)
        if cfg.pdfdoc:
            sys.stdout.write('\n')

    def __getitem__(self, index):
        if (index < 0) or (index >= len(cfg.pictureFiles)):
            if (index > len(cfg.pictureFiles)) or (cfg.blankslide == ''):
                buffer = '\0\0\0' * 320 * 240
                image = wx.ImageFromBuffer(320, 240, buffer)
                return image
            else:
                f = open(cfg.blankslide, 'rb')
                image = wx.ImageFromStream(f)
                image.Rescale(320, 240)
                f.close()
                return image

        return self.list[index]


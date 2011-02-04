# $Id: ImageList.py,v 1.2 2011-02-04 17:41:56 natano Exp $
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

import sys
import threading
from Queue import Queue
from cStringIO import StringIO

import wx
import cairo

from DouF00 import appcfg


class ImageList(list):
    def __init__(self, imagelist_name, images_size=None):
        super(ImageList, self).__init__()
        if appcfg.blankslide == '':
            buffer = '\0\0\0' * 320 * 240
            self.blank = wx.ImageFromBuffer(320, 240, buffer)
        elif appcfg.blankslide[0] == 'image':
            f = open(appcfg.blankslide[1], 'rb')
            self.blank = wx.ImageFromStream(f)
            f.close()
        elif appcfg.blankslide[0] == 'PDF':
            f = self.loadPdfPage(appcfg.blankslide[1])
            self.blank = wx.ImageFromStream(f)
            f.close()
        else:
            raise KeyError('Unknown blank slide format')

        slidecount = len(appcfg.pictureFiles)
        for i, j in enumerate(appcfg.pictureFiles):
            sys.stdout.write('\r* Loading {0}: {1:03}/{2:03} '.format(
                imagelist_name, i+1, slidecount))
            sys.stdout.flush()

            image = self.loadImage(i)
            if images_size:
                image = image.scaleTo(images_size)
            self.append(image)

        sys.stdout.write('\n')

    def loadImage(self, slideindex):
        if appcfg.pdfdoc:
            f = self.loadPdfPage(appcfg.pictureFiles[slideindex])
        else:
            f = open(appcfg.pictureFiles[slideindex], 'rb')

        image = wx.ImageFromStream(f)
        f.close()
        return image

    def loadPdfPage(self, pagenum):
        page = appcfg.pdfdoc.get_page(pagenum)
        size = [int(n) for n in page.get_size()]
        img = cairo.ImageSurface(cairo.FORMAT_RGB24, *size)
        context = cairo.Context(img)
        context.set_source_rgb(1.0, 1.0, 1.0)
        context.rectangle(0, 0, *size)
        context.fill()
        page.render(context)
        f = StringIO()
        img.write_to_png(f)
        f.seek(0)
        return f

    def __getitem__(self, slideindex):
        if (slideindex < 0) or (slideindex == len(self)):
            return self.blank

        elif slideindex > len(self):
            buffer = '\0\0\0' * 320 * 240
            return wx.ImageFromBuffer(320, 240, buffer)

        return super(ImageList, self).__getitem__(slideindex)


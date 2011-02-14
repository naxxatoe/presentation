# $Id: MyImage.py,v 1.5 2011-02-02 16:49:06 natano Exp $
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

import wx

from DouF00 import appcfg


def makeImageBorder(self, pixels=5):
    img = self.Copy()
    color = appcfg.presentorBorderColor
    size = img.GetSize()
    for (x, y, width, height) in [(0, 0,                size[0], pixels ),
                                  (0, 0,                pixels,  size[1]),
                                  (0, size[1] - pixels, size[0], pixels ),
                                  (size[0] - pixels, 0, pixels,  size[1])]:
        rect = wx.Rect(x, y, width, height)
        img.SetRGBRect(rect, color[0], color[1], color[2])

    return img

def scaleTo(self, size, method='scale'):
    imageSize = self.GetSize()
    if method == 'stretch':
        imageSize = size
    else:
        ratioX = float(size[0]) / imageSize[0]
        ratioY = float(size[1]) / imageSize[1]
        ratio = min(ratioX, ratioY)
        imageSize = [n * ratio for n in imageSize]

    return self.Scale(*imageSize)

def scaleImageToBitmap(self, size, method='scale'):
    image = self.scaleTo(size, method=method)
    return wx.BitmapFromImage(image)

wx.Image.makeImageBorder = makeImageBorder
wx.Image.scaleTo = scaleTo
wx.Image.scaleImageToBitmap = scaleImageToBitmap


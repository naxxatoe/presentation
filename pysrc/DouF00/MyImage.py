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

def makeImageBorder(self, pixels = 5):
    img = self.Copy()
    color = cfg.presentorBorderColor
    size = img.GetSize()
    for (x, y, width, height) in [(0, 0,                size[0], pixels ),
                                  (0, 0,                pixels,  size[1]),
                                  (0, size[1] - pixels, size[0], pixels ),
                                  (size[0] - pixels, 0, pixels,  size[1])]:
        rect = wx.Rect(x, y, width, height)
        img.SetRGBRect(rect, color[0], color[1], color[2])

    return img

def scaleImageToBitmap(self, size, method = "scale"):
    ImageSize = self.GetSize()
    if method == "stretch":
        ImageSize = size
    else:
        ratioX = float(size[0]) / ImageSize[0]
        ratioY = float(size[1]) / ImageSize[1]
        if ratioX < ratioY:
            ImageSize[0] = int(ImageSize[0] * ratioX)
            ImageSize[1] = int(ImageSize[1] * ratioX)
        else:
            ImageSize[0] = int(ImageSize[0] * ratioY)
            ImageSize[1] = int(ImageSize[1] * ratioY)
                
    image = self.Scale(ImageSize[0], ImageSize[1])
    bitmap = wx.BitmapFromImage(image)

    return bitmap

wx.Image.makeImageBorder = makeImageBorder
wx.Image.scaleImageToBitmap = scaleImageToBitmap


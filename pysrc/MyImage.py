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


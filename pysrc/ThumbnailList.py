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
import threading
import config as cfg

class ThumbnailList(list):
    def __init__(self):
        super(ThumbnailList, self).__init__()
        self.list = []
        for filename in cfg.pictureFiles:
            f = open(filename, "rb")
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

    def __getitem__(self, index):
        if (index < 0) or (index >= len(cfg.pictureFiles)):
            if (index > len(cfg.pictureFiles)) or (cfg.blankslide == ""):
                buffer = "\0\0\0" * 320 * 240
                image = wx.ImageFromBuffer(320, 240, buffer)
                return image
            else:
                f = open(cfg.blankslide, "rb")
                image = wx.ImageFromStream(f)
                image.Rescale(320, 240)
                f.close()
                return image

        return self.list[index]


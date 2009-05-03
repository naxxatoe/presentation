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


import wx

def scaleImage(image, size, method = "scale"):
    ImageSize = image.GetSize()
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
                
    image.Rescale(ImageSize[0], ImageSize[1])
    bitmap = wx.BitmapFromImage(image)

    return bitmap


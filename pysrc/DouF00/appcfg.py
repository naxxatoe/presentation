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
import os

title = 'DouF00'
__version__ = '2.0.0'
__author__ = 'Martin Ptacek'
numberFontSize = 150
preLoadCache = 5
pictureFiles = None
blankslide = None
slidelist = None
thumbnaillist = None
EVT_CLOCK_ID = wx.NewId()
pause = False
index = False
presentorBackgroundColor = wx.Color(80, 80, 80)
presentorBorderColor = (255, 0, 0)
blankThumbnail = None
pdfdoc = None
pdfpass = ''

filetypes = (
    ('JPEG', '\xff\xd8'),
    ('PNG', '\x89PNG\x0d\x0a\x1a\x0a'),
    ('BMP', 'BM'),
    ('PCX', '\x0a'),
    ('PDF', '\x25\x50\x44\x46'),
)

configFile = os.path.expanduser('~/.douf00/douf00.conf')


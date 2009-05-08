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

title = "DouF00"
__version__ = "1.0"
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

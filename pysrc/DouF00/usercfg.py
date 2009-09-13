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

import appcfg
import ConfigParser

defaults = {
    'blankSlide': '',
    'exitAfterLastSlide': 'False',
    'preDouF00': '',
    'postDouF00': '',
    'time': '45',
    'slidePath': '',
    'blankpage': '0',
}

config = {}

def parseConfig():
    try:
        f = open(appcfg.configFile, 'r')
        cfg = ConfigParser.SafeConfigParser(defaults)
        cfg.readfp(f)
        f.close

        config['blankSlide'] = cfg.get('general', 'blankSlide')
        config['exitAfterLastSlide'] = cfg.getboolean('general', 'exitAfterLastSlide')
        config['preDouF00'] = cfg.get('general', 'preDouF00')
        config['postDouF00'] = cfg.get('general', 'postDouF00')
        config['time'] = cfg.getint('general', 'time')
        config['slidePath'] = cfg.get('general', 'slidePath')
        config['blankpage'] = cfg.getint('general', 'blankpage')

    except IOError:
        pass

    except ConfigParser.NoSectionError:
        pass


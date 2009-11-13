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
    'blankslide': '',
    'exitafterlastslide': 'False',
    'predouf00': '',
    'postdouf00': '',
    'time': '45',
    'slidepath': '',
    'blankpage': '0',
    'password': 'False',
}

config = defaults.copy()

def parseConfig():
    cfg = ConfigParser.SafeConfigParser(defaults)
    try:
        f = open(appcfg.configFile, 'r')
        cfg.readfp(f)
        try:
            userconfig = cfg.items('general')
            for item in userconfig:
                key, value = item
                if value:
                    config[key] = value

        except ConfigParser.NoSectionError:
            print "Config file error"
            sys.exit(1)

        f.close

    except IOError:
        pass

    for key in ('exitafterlastslide', 'password', 'autostart'):
        if config[key] == 'True':
            config[key] = True
        elif config[key] == 'False':
            config[key] = False
        else:
            print "Config file error"
            sys.exit(1)

    for key in ('presentor', 'audience'):
       if key in config:
           config[key] = config[key].split(' ').split('\t')

    for key in ('time', 'blankpage'):
        try:
            config[key] = int(config[key])
        except ValueError:
            print "Config file error"
            sys.exit(1)


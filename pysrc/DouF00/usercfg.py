# $Id: usercfg.py,v 1.4 2011-02-01 14:04:56 natano Exp $
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

import sys
import ConfigParser

from DouF00 import appcfg

defaults = {
    'blankslide': '',
    'exitafterlastslide': 'False',
    'predouf00': '',
    'postdouf00': '',
    'time': '45',
    'slidepath': '',
    'blankpage': '0',
    'password': 'False',
    'autostart': 'False',
    'presentor': '',
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
           config[key] = config[key].split(' ')

    for key in ('time', 'blankpage'):
        try:
            config[key] = int(config[key])
        except ValueError:
            print "Config file error"
            sys.exit(1)


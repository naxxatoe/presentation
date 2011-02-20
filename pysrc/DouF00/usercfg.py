# $Id: usercfg.py,v 1.4 2011-02-20 01:38:12 natano Exp $
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

from DouF00 import appcfg
from DouF00.OptionParser import *

_options = OptList(
    IntOpt('t', 'time', 'time', 45, 'presentation time'),
    IntOpt('B', 'blankpage', 'blankpage', 0,
        'page of PDF file to use as blank slide'),
    BoolOpt('e', 'exit', 'exitafterlastslide', False,
        'exit after the last slide'),
    BoolOpt('S', 'password', 'password', False,
        'PDF file is password protected'),
    BoolOpt('a', 'autostart', 'autostart', False,
        'automatically start presentation'),
    ArrOpt(None, None, 'presentor', [],
        'Display numbers to use as a presentors screen'),
    ArrOpt(None, None, 'audience', [],
        'Display numbers to use as an audience screen'),
    StrOpt('b', 'blank', 'blankslide', '', 'file to use as blank slide'),
    StrOpt('s', 'pre', 'predouf00', '',
        'command to be run when starting the application'),
    StrOpt('p', 'post', 'postdouf00', '',
        'command to be run after the application'),
    StrOpt(None, None, 'slidepath', '', 'The path for the slides'),
)

config = Options(_options, usage='%prog [options] [slidepath]',
    version=appcfg.__version__,
    mexclusive=(
        ('blankslide', 'blankpage'),
    ),
)


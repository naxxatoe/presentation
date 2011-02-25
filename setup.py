#!/usr/bin/env python
# $Id: setup.py,v 1.8 2011-02-25 19:46:26 natano Exp $
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

from distutils.core import setup
import os, platform

dirname = os.path.dirname(__file__)

osname = platform.system()
if osname == 'Linux':
    manpath = 'share/man/man1'
else:
    manpath = 'man/man1'

args = {
    'name': 'DouF00',
    'version': '3.0.2',
    'description': 'fat free presentations',

    'author': 'Martin Natano',
    'author_email': 'natanoptacek@gmail.com',
    'license': 'MIT',
    'url': 'http://www.natano.net/',

    'platforms': ['Linux'],
    'packages': ['DouF00'],
    'package_dir': {'DouF00': os.path.join(dirname, 'pysrc/DouF00')},
    'scripts': [os.path.join(dirname, 'pysrc/wrapper/douf00')],
    'data_files': [(manpath, [
        os.path.join(dirname, 'doc/douf00.1'),
    ])],
}

setup(**args)


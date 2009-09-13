#!/usr/bin/env python
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
# Email: natanoptacek@gmail.com
# Web: http://nicenamecrew.com/

from distutils.core import setup

args = {
    'name': 'DouF00',
    'version': '2.0.0',
    'description': 'fat free presentations',

    'author': 'Martin Ptacek',
    'author_email': 'natano@nicenamecrew.com',
    'license': 'MIT',
    'url': 'http://nicenamecrew.com/',

    'platforms': ['Linux'],
    'packages': ['DouF00'],
    'package_dir': {'DouF00': 'pysrc/DouF00'},
    'scripts': ['pysrc/wrapper/douf00'],
    'data_files': [('share/man/man1', ['doc/douf00.1'])],
}

setup(**args)


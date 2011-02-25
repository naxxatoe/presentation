# $Id: OptionParser.py,v 1.2 2011-02-25 18:02:35 natano Exp $
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

from __future__ import with_statement

import os, sys
import ConfigParser
from optparse import OptionParser

__all__ = ['BoolOpt', 'StrOpt', 'IntOpt', 'ArrOpt', 'OptList', 'Options']

class OptBase(object):
    opt_extra_kwargs = {}

    def __init__(self, sname, lname, cname, default, help=None):
        self.sname = sname
        self.lname = lname
        self.cname = cname
        self.default = default
        self.help = help

    def getOptparseArgs(self):
        if not self.sname:
            return None

        args = ['-%s' % (self.sname)]
        if self.lname:
            args.append('--%s' % (self.lname))

        kwargs = {'help': self.help, 'dest': self.cname}
        kwargs.update(self.opt_extra_kwargs)

        return (args, kwargs)

    def addOption(self, parser):
        args, kwargs = self.getOptparseArgs()
        parser.add_option(*args, **kwargs)

    def parseCf(self, v):
        return v

    def parseCl(self, v):
        return v

class BoolOpt(OptBase):
    opt_extra_kwargs = {'action': 'store_true'}

    def parseCf(self, v):
        if v.lower() == 'true':
            return True
        elif v.lower() == 'false':
            return False
        else:
            raise ValueError(
                'Invalid expression "%s" for boolean value' % (v))

class StrOpt(OptBase):
    opt_extra_kwargs = {'action': 'store'}

class IntOpt(OptBase):
    opt_extra_kwargs = {'action': 'store', 'type': 'int'}

    def parseCf(self, v):
        return int(v)

class ArrOpt(OptBase):
    opt_extra_kwargs = {'action': 'store'}

    def parseCf(self, v):
        return v.split(' ')

    def parseCl(self, v):
        return v.split(' ')

class OptList(list):
    def __init__(self, *args):
        super(OptList, self).__init__(args)

    def iterClOpts(self):
        for opt in self:
            if opt.sname:
                yield opt

class Options(dict):
    def die(self, message):
        print >>sys.stderr, 'Config file error: %s' % (message)
        sys.exit(1)

    def __init__(self, options, usage=None, version=None, mexclusive=None):
        super(Options, self).__init__()
        self.options = options
        self.usage = usage
        self.version = version
        self.mexclusive = mexclusive

        for opt in self.options:
            self[opt.cname] = opt.default

    def loadFile(self, fname):
        if not os.path.isfile(fname):
            return

        cfg = ConfigParser.SafeConfigParser()
        with open(fname, 'r') as f:
            cfg.readfp(f)

        for opt in self.options:
            try:
                v = cfg.get('general', opt.cname)
                try:
                    self[opt.cname] = opt.parseCf(v)
                except ValueError, e:
                    die('%s: %s' % (opt.cname, e))
            except ConfigParser.NoOptionError:
                pass
            except ConfigParser.NoSectionError:
                die('section "general" not found')

    def loadArgv(self, argv):
        parser = OptionParser(usage=self.usage, version=self.version,
            prog=os.path.basename(argv[0]))

        for opt in self.options.iterClOpts():
            opt.addOption(parser)

        options, args = parser.parse_args(argv[1:])
        for opt in self.options.iterClOpts():
            v = options.__dict__[opt.cname]
            if v == None:
                continue
            self[opt.cname] = opt.parseCl(v)

        for t in self.mexclusive:
            count = 0
            for cname in t:
                if options.__dict__[cname] is not None:
                    count += 1

            if count <= 1:
                continue

            parser.error('Options %s and %s are mutually exclusive' % (
                ', '.join(t[:-1]), t[-1]))

        return parser, args


#!/usr/bin/env python3
#
# Copyright (c) 2014-2018 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import TestSCons
import re
import sys
import os

if sys.platform == 'win32':
    test = TestSCons.TestSCons(program='scons.bat', interpreter=None)
else:
    test = TestSCons.TestSCons()

test.subdir(['bin'])

test.write('bin/hammer.py', """\
#!%s
import sys
with open(sys.argv[1], 'w') as target:
    with open(sys.argv[2], 'r') as source:
      target.write(source.read().replace('nail', 'drived in nail'))
""" % sys.executable)

# bat file for win32
test.write('bin/hammer.bat', """\
@echo off
%s %s %%*
""" % (sys.executable, test.workpath('bin/hammer.py')))

# shell script for posix
test.write('bin/hammer', """\
#!/usr/bin/env sh
%s %s "$@"
""" % (sys.executable, test.workpath('bin/hammer.py')))
os.chmod(test.workpath('bin/hammer'), 0o755)

test.subdir(['site_scons'])
test.subdir(['site_scons', 'site_tools'])
test.write('site_scons/site_tools/hammer.py', r"""\
from sconstool.util import *
from SCons.Builder import Builder

find_hammer = ToolFinder('hammer')

def generate(env):
    env['HAMMER'] = find_hammer(env)
    env['HAMMERCOM'] = '$HAMMER $TARGET $SOURCE'
    env['BUILDERS']['Hammer'] = Builder(action='$HAMMERCOM')

def exists(env):
    return find_hammer(env)
""")

test.write('hammer.in', """\
We have twenty nails.
""")

test.write('SConstruct', r"""\
env = Environment(tools=[])
env.PrependENVPath('PATH', %(bindir)r)
env.Tool('hammer')
tgt = env.Hammer('hammer.out', 'hammer.in')
""" % {'bindir': test.workpath('bin')})

test.run(['-Q'])

test.must_exist('hammer.out')
test.must_contain('hammer.out', r"We have twenty drived in nails")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

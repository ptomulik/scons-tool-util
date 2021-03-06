# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (c) 2014-2020 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>
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

"""Ensure that the toolfinder/iconv example from user documentation works"""

import TestSCons
import re
import sys
import os

if sys.platform == 'win32':
    test = TestSCons.TestSCons(program='scons.bat', interpreter=None)
else:
    test = TestSCons.TestSCons()

if sys.version_info < (3,0):
    from io import open as uopen
else:
    uopen = open

if not test.where_is('iconv'):
    test.skip_test("Could not find 'iconv', skipping test(s).\n")

test.dir_fixture('../../../../../docs/user/utils/toolfinder/iconv')

test.run()
test.must_contain_all_lines(test.stdout(), ['iconv -f LATIN2 -t UTF-8 latin2.txt > utf8.txt'])

test.must_exist('utf8.txt')
with uopen(test.workpath('latin2.txt'), 'r', encoding='latin2') as f:
    latin2 = f.read()

with uopen(test.workpath('utf8.txt'), 'r', encoding='utf8') as f:
    utf8 = f.read()
test.must_contain_exactly_lines(utf8, latin2.splitlines())

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

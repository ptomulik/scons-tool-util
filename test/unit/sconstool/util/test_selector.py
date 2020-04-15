# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-2020 Paweł Tomulik
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

import sys
import os
import string
if sys.version_info < (3,0):
    import unittest2 as unittest
    import mock
else:
    import unittest
    import unittest.mock as mock

import sconstool.util.selector_ as selector_

class _Environment(dict):
    def subst(self, s):
        new = string.Template(s).safe_substitute(self)
        while new != s:
            s = new
            new = string.Template(s).safe_substitute(self)
        return new


class _Node(object):
    def __init__(self, path):
        self.path = path
    def __str__(self):
        return str(self.path)


class SelectorTests(unittest.TestCase):

    def test__getitem__(self):
        s = selector_.Selector({'a': 'AAA', 'b': 'BBB'})
        self.assertEqual(s['a'], 'AAA')
        self.assertEqual(s['b'], 'BBB')

    def test__getitem__KeyError(self):
        s = selector_.Selector({'a': 'AAA', 'b': 'BBB'})
        with self.assertRaises(KeyError) as context:
            s['c']

    def test__setitem__(self):
        s = selector_.Selector({'a': 'AAA', 'b': 'BBB'})
        s['c'] = 'CCC'
        self.assertEqual(s['c'], 'CCC')

    def test__call__literal(self):
        env = _Environment()
        s = selector_.Selector({'.d': 'DDD', '.e': 'EEE'})

        ret = s(env, [])
        self.assertIsNone(ret)

        ret = s(env, [_Node('foo.d')])
        self.assertEqual(ret, 'DDD')

        ret = s(env, [_Node('bar.e')])
        self.assertEqual(ret, 'EEE')

        ret = s(env, [_Node('bar.x')])
        self.assertIsNone(ret)

        s[None] = 'XXX'
        ret = s(env, [_Node('bar.x')])
        self.assertEqual(ret, 'XXX')

    def test__call__subst(self):
        env = _Environment({'FSUFF': '.f', 'GSUFF': '.g'})

        s = selector_.Selector({'$FSUFF': 'FFF', '$GSUFF': 'GGG'})
        ret = s(env, [_Node('foo.f')])
        self.assertEqual(ret, 'FFF')

        ret = s(env, [_Node('bar.g')])
        self.assertEqual(ret, 'GGG')

    def test__call__literal_over_subst(self):
        env = _Environment({'FSUFF': '.f', 'GSUFF': '.g'})
        s = selector_.Selector({'$FSUFF': 'SUBFFF', '.f': 'LITFFF', '$GSUFF': 'SUBGGG'})

        ret = s(env, [_Node('foo.f')])
        self.assertEqual(ret, 'LITFFF')

        ret = s(env, [_Node('foo.g')])
        self.assertEqual(ret, 'SUBGGG')

    def test__call__subst_no_ambiguity(self):
        env = _Environment({'FSUFF1': '.f', 'FSUFF2': '.f'})
        s = selector_.Selector({'$FSUFF1': 'SUBFFF1', '.f': 'LITFFF'})
        ret = s(env, [_Node('foo.f')])
        self.assertEqual(ret, 'LITFFF')

    def test__call__subst_ambiguity(self):
        env = _Environment({'FSUFF1': '.f', 'FSUFF2': '.f'})
        s = selector_.Selector({'$FSUFF1': 'SUBFFF1', '$FSUFF2': 'SUBSUFF2', '.f': 'LITFFF'})

        with self.assertRaises(KeyError) as context:
            s(env, [_Node('foo.f')])
        exc = context.exception
        self.assertIn(exc.args[0], ('$FSUFF1', '$FSUFF2'))
        if exc.args[0] == '$FSUFF1':
            self.assertEqual(exc.args[1], '$FSUFF2')
        else:
            self.assertEqual(exc.args[1], '$FSUFF1')
        self.assertEqual(exc.args[2], '.f')

    def test__call__longest_wins(self):
        env = _Environment({'THSUF': '.t.h', 'XTHSUFF': '.x.t.h'})
        s = selector_.Selector({'$THSUFF': 'SUBTH', '$XTHSUFF': 'SUBXTH', '.h': 'LITH', '.t.h': 'LITTH'})

        ret = s(env, [_Node('foo.h')])
        self.assertEqual(ret, 'LITH')

        ret = s(env, [_Node('foo.t.h')])
        self.assertEqual(ret, 'LITTH')

        ret = s(env, [_Node('foo.x.t.h')])
        self.assertEqual(ret, 'SUBXTH')

    def test__call__ext(self):
        env = _Environment({'THSUF': '.t.h', 'XTHSUFF': '.x.t.h'})
        s = selector_.Selector({'$THSUFF': 'SUBTH', '$XTHSUFF': 'SUBXTH', '.h': 'LITH', '.t.h': 'LITTH'})

        ret = s(env, [], '.h')
        self.assertEqual(ret, 'LITH')

        ret = s(env, [], '.t.h')
        self.assertEqual(ret, 'LITTH')

        ret = s(env, [], '.x.t.h')
        self.assertEqual(ret, 'SUBXTH')

        ret = s(env, [], '.f')
        self.assertIsNone(ret)

    def test__call__source_without_nosuffix(self):
        env = _Environment()

        s = selector_.Selector({'.f': 'FFF', '.g': 'GGG'})
        ret = s(env, [_Node('foo')])
        self.assertIsNone(ret)

        s = selector_.Selector({None: 'XXX', '.f': 'FFF', '.g': 'GGG'})
        ret = s(env, [_Node('foo')])
        self.assertEqual(ret, 'XXX')

    def test__call__ext_empty(self):
        env = _Environment()

        s = selector_.Selector({'.f': 'FFF', '.g': 'GGG'})
        ret = s(env, [], '')
        self.assertIsNone(ret)

        s = selector_.Selector({None: 'XXX', '.f': 'FFF', '.g': 'GGG'})
        ret = s(env, [], '')
        self.assertEqual(ret, 'XXX')

        s = selector_.Selector({None: 'XXX', '': 'YYY', '.f': 'FFF', '.g': 'GGG'})
        ret = s(env, [], '')
        self.assertEqual(ret, 'YYY')

    def test__call__source_empty(self):
        env = _Environment()

        s = selector_.Selector({'.f': 'FFF', '.g': 'GGG'})
        ret = s(env, [])
        self.assertIsNone(ret)

        s = selector_.Selector({None: 'XXX', '.f': 'FFF', '.g': 'GGG'})
        ret = s(env, [])
        self.assertEqual(ret, 'XXX')

        s = selector_.Selector({None: 'XXX', '': 'YYY', '.f': 'FFF', '.g': 'GGG'})
        ret = s(env, [])
        self.assertEqual(ret, 'YYY')


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

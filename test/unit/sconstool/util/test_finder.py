# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Paweł Tomulik
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
from string import Template
if sys.version_info < (3, 0):
    import unittest2 as unittest
    import mock
else:
    import unittest
    import unittest.mock as mock

import sconstool.util.finder_ as finder_
import sconstool.util.misc_ as misc_


def _p(p):
    pieces = p.split(r'/')
    if sys.platform == 'win32' and pieces and not pieces[0]:
        pieces[0] = 'C:'
    return os.path.sep.join(pieces)


class _Environment(dict):
    _default_existing_files = [
        _p('/opt/bin/python'),
        _p('/opt/bin/xyz'),
        _p('/usr/bin/gcc'),
        _p('/usr/bin/python'),
        _p('/usr/bin/python3'),
        _p('/some/where/python'),
        _p('/some/where/puppet')
    ]

    def __init__(self, existing_files=None, *args, **kw):
        if existing_files is None:
            existing_files = self._default_existing_files
        self._existing_files = existing_files
        dict.__init__(self, *args, **kw)

    def subst(self, string):
        new = Template(string).safe_substitute(self)
        while new != string:
            string = new
            new = Template(string).safe_substitute(self)
        return new

    def WhereIs(self, prog, path=None, pathext=None, reject=[]):
        if path is None:
            path = [_p('/usr/local/bin'), _p('/usr/bin')]
        elif isinstance(path, str):
            path = self.subst(path).split(os.path.pathsep)

        if pathext is None:
            pathext = self.get('ENV', dict()).get('PATHEXT')
        elif isinstance(pathext, str):
            pathext = self.subst(pathext)

        for dir in path:
            full = os.path.join(dir, prog)
            if full in self._existing_files:
                return full
        return None


class ToolFinderTests(unittest.TestCase):
    _ctor_kwargs = ('name',
                    'path',
                    'pathext',
                    'reject',
                    'priority_path',
                    'fallback_path',
                    'strip_path',
                    'strip_priority_path',
                    'strip_fallback_path')

    def test__ctor_kwargs(self):
        self.assertEqual(finder_.ToolFinder._ctor_kwargs, self._ctor_kwargs)

    def test__init(self):
        with mock.patch('sconstool.util.misc_.check_kwargs') as check_kwargs:
            kw = {'a': 'A', 'b': 'B' }
            w = finder_.ToolFinder('xxx', **kw)
            check_kwargs.assert_called_once_with('ToolFinder()', kw, self._ctor_kwargs)
            self.assertEqual(w._tool, 'xxx')
            self.assertEqual(w._kw, kw)

    def test__tool(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.tool, 'xxx')

    def test__tool__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').tool = 'yyy'
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__name(self):
        w = finder_.ToolFinder('xxx', name='yyy')
        self.assertEqual(w.name, 'yyy')

    def test__name__dollar(self):
        w = finder_.ToolFinder('xxx', name='$YYY')
        self.assertEqual(w.name, '$YYY')

    def test__name__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.name, 'xxx')

    def test__name__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').name = ''
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__path(self):
        w = finder_.ToolFinder('xxx', path='yyy')
        self.assertEqual(w.path, 'yyy')

    def test__path__dollar(self):
        w = finder_.ToolFinder('xxx', path='$YYY')
        self.assertEqual(w.path, '$YYY')

    def test__path__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertIsNone(w.path)

    def test__path__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').path = ''
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__pathext(self):
        w = finder_.ToolFinder('xxx', pathext='yyy')
        self.assertEqual(w.pathext, 'yyy')

    def test__pathext__dollar(self):
        w = finder_.ToolFinder('xxx', pathext='$YYY')
        self.assertEqual(w.pathext, '$YYY')

    def test__pathext__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertIsNone(w.pathext)

    def test__pathext__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').pathext = ''
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__reject(self):
        w = finder_.ToolFinder('xxx', reject='yyy')
        self.assertEqual(w.reject, 'yyy')

    def test__reject__dollar(self):
        w = finder_.ToolFinder('xxx', reject='$YYY')
        self.assertEqual(w.reject, '$YYY')

    def test__reject__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.reject, [])

    def test__reject__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').reject = ''
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__priority_path(self):
        w = finder_.ToolFinder('xxx', priority_path='yyy')
        self.assertEqual(w.priority_path, 'yyy')

    def test__priority_path__dollar(self):
        w = finder_.ToolFinder('xxx', priority_path='$YYY')
        self.assertEqual(w.priority_path, '$YYY')

    def test__priority_path__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.priority_path, [])

    def test__priority_path__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').priority_path = ''
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__fallback_path(self):
        w = finder_.ToolFinder('xxx', fallback_path='yyy')
        self.assertEqual(w.fallback_path, 'yyy')

    def test__fallback_path__dollar(self):
        w = finder_.ToolFinder('xxx', fallback_path='$YYY')
        self.assertEqual(w.fallback_path, '$YYY')

    def test__fallback_path__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.fallback_path, [])

    def test__fallback_path__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').fallback_path = ''
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__strip_path(self):
        w = finder_.ToolFinder('xxx', strip_path=True)
        self.assertTrue(w.strip_path)

    def test__strip_path__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertTrue(w.strip_path)

    def test__strip_path__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').strip_path = True
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__strip_priority_path(self):
        w = finder_.ToolFinder('xxx', strip_priority_path=True)
        self.assertTrue(w.strip_priority_path)

    def test__strip_priority_path__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertFalse(w.strip_priority_path)

    def test__strip_priority_path__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').strip_priority_path = True
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__strip_fallback_path(self):
        w = finder_.ToolFinder('xxx', strip_fallback_path=True)
        self.assertTrue(w.strip_fallback_path)

    def test__strip_fallback_path__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertFalse(w.strip_fallback_path)

    def test__strip_fallback_path__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').strip_fallback_path = True
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__adjust_result(self):
        env = _Environment()

        find = finder_.ToolFinder('gcc')
        self.assertEqual(find._adjust_result(env, ('gcc', _p('/usr/bin/gcc')), 'path'), 'gcc')

        find = finder_.ToolFinder('gcc', strip_path=False)
        self.assertEqual(find._adjust_result(env, ('gcc', _p('/usr/bin/gcc')), 'path'), _p('/usr/bin/gcc'))

    def test__adjust_result__extra_paths(self):
        env = _Environment()

        pp = os.path.pathsep.join([_p('/opt/local/bin'), _p('/opt/bin')])
        fp = os.path.pathsep.join([_p('/some/local/where'), _p('/some/where')])

        find = finder_.ToolFinder('python', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._adjust_result(env, ('python', _p('/opt/bin/python')), 'priority_path'), _p('/opt/bin/python'))
        self.assertEqual(find._adjust_result(env, ('python', _p('/usr/bin/python')), 'path'), 'python')
        self.assertEqual(find._adjust_result(env, ('python', _p('/some/where/python')), 'fallback_path'), _p('/some/where/python'))

        find = finder_.ToolFinder('python', priority_path=pp, strip_path=False,
                                  strip_priority_path=True, strip_fallback_path=True)
        self.assertEqual(find._adjust_result(env, ('python', _p('/opt/bin/python')), 'priority_path'), 'python')
        self.assertEqual(find._adjust_result(env, ('python', _p('/usr/bin/python')), 'path'), _p('/usr/bin/python'))
        self.assertEqual(find._adjust_result(env, ('python', _p('/some/where/python')), 'fallback_path'), 'python')

    def test__adjust_result__absname__strip(self):
        env = _Environment()

        find = finder_.ToolFinder('python', name=_p('/foo/bar/python'), strip_path=True,
                                  strip_priority_path=True, strip_fallback_path=True)
        # absolute path given as *name* is over the strip_* settings
        self.assertEqual(find._adjust_result(env, (_p('/foo/bar/python'), _p('/opt/bin/python')), 'priority_path'), _p('/foo/bar/python'))
        self.assertEqual(find._adjust_result(env, (_p('/foo/bar/python'), _p('/usr/bin/python')), 'path'), _p('/foo/bar/python'))
        self.assertEqual(find._adjust_result(env, (_p('/foo/bar/python'), _p('/some/where/python')), 'fallback_path'), _p('/foo/bar/python'))

    def test__search_in(self):
        env = _Environment()

        pp = os.path.pathsep.join([_p('/opt/local/bin'), _p('/opt/bin')])
        fp = os.path.pathsep.join([_p('/some/local/where'), _p('/some/where')])

        find = finder_.ToolFinder('python', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search_in(env, 'priority_path'), _p('/opt/bin/python'))
        self.assertEqual(find._search_in(env, 'path'), 'python')
        self.assertEqual(find._search_in(env, 'fallback_path'), _p('/some/where/python'))

        find = finder_.ToolFinder('python', priority_path=pp, fallback_path=fp, strip_path=False,
                                  strip_priority_path=True, strip_fallback_path=True)
        self.assertEqual(find._search_in(env, 'priority_path'), 'python')
        self.assertEqual(find._search_in(env, 'path'), _p('/usr/bin/python'))
        self.assertEqual(find._search_in(env, 'fallback_path'), 'python')

    def test__search_in__multiple_names(self):
        env = _Environment()

        pp = os.path.pathsep.join([_p('/opt/local/bin'), _p('/opt/bin')])
        fp = os.path.pathsep.join([_p('/some/local/where'), _p('/some/where')])

        find = finder_.ToolFinder('python', name=['python3', 'python'], priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search_in(env, 'priority_path'), _p('/opt/bin/python'))
        self.assertEqual(find._search_in(env, 'path'), 'python3')
        self.assertEqual(find._search_in(env, 'fallback_path'), _p('/some/where/python'))

    def test__search_in__path_list(self):
        env = _Environment()

        pp = [_p('/opt/local/bin'), _p('/opt/bin')]
        fp = [_p('/some/local/where'), _p('/some/where')]

        find = finder_.ToolFinder('python', name=['python3', 'python'], priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search_in(env, 'priority_path'), _p('/opt/bin/python'))
        self.assertEqual(find._search_in(env, 'path'), 'python3')
        self.assertEqual(find._search_in(env, 'fallback_path'), _p('/some/where/python'))

    def test__search_in__subst(self):
        env = _Environment(OPTLOCAL=_p('$OPT/local/bin'), OPT=_p('/opt'), SOMELOCAL=_p('$SOME/local'), SOME=_p('/some'))

        pp = os.path.pathsep.join([_p('$OPTLOCAL/bin'), _p('$OPT/bin')])
        fp = os.path.pathsep.join([_p('$SOMELOCAL/where'), _p('$SOME/where')])

        find = finder_.ToolFinder('python', name=['python3', 'python'], priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search_in(env, 'priority_path'), _p('/opt/bin/python'))
        self.assertEqual(find._search_in(env, 'path'), 'python3')
        self.assertEqual(find._search_in(env, 'fallback_path'), _p('/some/where/python'))

    def test__search_in__path_list__subst(self):
        env = _Environment(OPTLOCAL=_p('$OPT/local/bin'), OPT=_p('/opt'), SOMELOCAL=_p('$SOME/local'), SOME=_p('/some'))

        pp = [_p('$OPTLOCAL/bin'), _p('$OPT/bin')]
        fp = [_p('$SOMELOCAL/where'), _p('$SOME/where')]

        find = finder_.ToolFinder('python', name=['python3', 'python'], priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search_in(env, 'priority_path'), _p('/opt/bin/python'))
        self.assertEqual(find._search_in(env, 'path'), 'python3')
        self.assertEqual(find._search_in(env, 'fallback_path'), _p('/some/where/python'))

    def test__search(self):
        env = _Environment()

        pp = os.path.pathsep.join([_p('/opt/local/bin'), _p('/opt/bin')])
        fp = os.path.pathsep.join([_p('/some/local/where'), _p('/some/where')])

        find = finder_.ToolFinder('python', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search(env), _p('/opt/bin/python'))

        find = finder_.ToolFinder('gcc', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search(env), 'gcc')

        find = finder_.ToolFinder('gcc', strip_path=False, priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search(env), _p('/usr/bin/gcc'))

        find = finder_.ToolFinder('puppet', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search(env), _p('/some/where/puppet'))

        find = finder_.ToolFinder('puppet', strip_fallback_path=True, priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search(env), 'puppet')

        find = finder_.ToolFinder('inexistent')
        self.assertIsNone(find._search(env))

    def test__call(self):
        env = _Environment()
        # We've already tested _search...
        with mock.patch.object(finder_.ToolFinder, '_search', return_value='ok') as _search:
            find = finder_.ToolFinder('foo')
            self.assertEqual(find(env), 'ok')
            _search.assert_called_once_with(env)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

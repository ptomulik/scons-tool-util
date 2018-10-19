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

import unittest
import unittest.mock as mock
import sconstool.util.finder_ as finder_
import sconstool.util.misc_ as misc_


class ToolFinderTests(unittest.TestCase):
    _ctor_kwargs = ('name',
                    'path',
                    'pathext',
                    'reject',
                    'priority_path',
                    'fallback_path',
                    'use_vars',
                    'use_name_var',
                    'use_priority_path_var',
                    'use_fallback_path_var',
                    'strip_path',
                    'strip_priority_path',
                    'strip_fallback_path',
                    'templates')

    _default_templates = {
        'name':          '$%(TOOL)sNAME',
        'priority_path': '$%(TOOL)sPRIORITYPATH',
        'fallback_path': '$%(TOOL)sFALLBACKPATH',
    }

    def test__ctor_kwargs(self):
        self.assertEqual(finder_.ToolFinder._ctor_kwargs, self._ctor_kwargs)

    def test__default_templates(self):
        self.assertEqual(finder_.ToolFinder._default_templates, self._default_templates)

    def test__init(self):
        with mock.patch('sconstool.util.misc_.check_kwargs') as check_kwargs:
            kw = {'a': 'A', 'b': 'B' }
            w = finder_.ToolFinder('xxx', **kw)
            check_kwargs.assert_called_once_with('ToolFinder()', kw, self._ctor_kwargs)
            self.assertEqual(w._tool, 'xxx')
            self.assertEqual(w._kw, kw)
            self.assertEqual(w._templates, w._default_templates)

    def test__tool(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.tool, 'xxx')

    def test__tool__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').tool = 'yyy'
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__default_name(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.default_name, 'xxx')

    def test__default_name___use_name_var(self):
        w = finder_.ToolFinder('xxx', use_name_var=True)
        self.assertEqual(w.default_name, '$XXXNAME')

    def test__default_name___use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=True)
        self.assertEqual(w.default_name, '$XXXNAME')

    def test__default_name___use_vars_and_use_name_var(self):
        w = finder_.ToolFinder('xxx', use_vars=False, use_name_var=True)
        self.assertEqual(w.default_name, '$XXXNAME')
        w = finder_.ToolFinder('xxx', use_vars=True, use_name_var=False)
        self.assertEqual(w.default_name, 'xxx')

    def test__name(self):
        w = finder_.ToolFinder('xxx', name='yyy')
        self.assertEqual(w.name, 'yyy')

    def test__name__dollar(self):
        w = finder_.ToolFinder('xxx', name='$YYY')
        self.assertEqual(w.name, '$YYY')

    def test__name__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.name, 'xxx')

    def test__name___use_name_var(self):
        w = finder_.ToolFinder('xxx', name='yyy', use_name_var=True)
        self.assertEqual(w.name, 'yyy')

    def test__name__default_with_name_var(self):
        w = finder_.ToolFinder('xxx', use_name_var=True)
        self.assertEqual(w.name, "$XXXNAME")

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

    def test__default_priority_path(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.default_priority_path, [])

    def test__default_priority_path__use_priority_path_var(self):
        w = finder_.ToolFinder('xxx', use_priority_path_var=True)
        self.assertEqual(w.default_priority_path, '$XXXPRIORITYPATH')

    def test__default_priority_path__use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=True)
        self.assertEqual(w.default_priority_path, '$XXXPRIORITYPATH')

    def test__default_priority_path__use_priority_path_var_and_use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=False, use_priority_path_var=True)
        self.assertEqual(w.default_priority_path, '$XXXPRIORITYPATH')
        w = finder_.ToolFinder('xxx', use_vars=True, use_priority_path_var=False)
        self.assertEqual(w.default_priority_path, [])

    def test__default_priority_path__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').default_priority_path = ''
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

    def test__default_fallback_path(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.default_fallback_path, [])

    def test__default_fallback_path__use_fallback_path_var(self):
        w = finder_.ToolFinder('xxx', use_fallback_path_var=True)
        self.assertEqual(w.default_fallback_path, '$XXXFALLBACKPATH')

    def test__default_fallback_path__use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=True)
        self.assertEqual(w.default_fallback_path, '$XXXFALLBACKPATH')

    def test__default_fallback_path__use_fallback_path_var_and_use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=False, use_fallback_path_var=True)
        self.assertEqual(w.default_fallback_path, '$XXXFALLBACKPATH')
        w = finder_.ToolFinder('xxx', use_vars=True, use_fallback_path_var=False)
        self.assertEqual(w.default_fallback_path, [])

    def test__default_fallback_path__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').default_fallback_path = ''
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

##    def test__name_var(self):
##        w = finder_.ToolFinder('xxx')
##        self.assertEqual(w.name_var, 'XXXNAME')
##
##    def test__name_var___template(self):
##        w = finder_.ToolFinder('xxx', templates={'name': '%(tool)sYYY'})
##        self.assertEqual(w.name_var, 'XXXYYY')
##
##    def test__name_var__setter(self):
##        with self.assertRaises(AttributeError) as context:
##            finder_.ToolFinder('xxx').name_var = True
##        self.assertEqual(str(context.exception), "can't set attribute")
##
##    def test__priority_path_var(self):
##        w = finder_.ToolFinder('xxx')
##        self.assertEqual(w.priority_path_var, 'XXXPRIORITYPATH')
##
##    def test__priority_path_var___template(self):
##        w = finder_.ToolFinder('xxx', templates={'priority_path': '%(tool)sYYY'})
##        self.assertEqual(w.priority_path_var, 'XXXYYY')
##
##    def test__priority_path_var__setter(self):
##        with self.assertRaises(AttributeError) as context:
##            finder_.ToolFinder('xxx').priority_path_var = True
##        self.assertEqual(str(context.exception), "can't set attribute")
##
##    def test__fallback_path_var(self):
##        w = finder_.ToolFinder('xxx')
##        self.assertEqual(w.fallback_path_var, 'XXXFALLBACKPATH')
##
##    def test__fallback_path_var___template(self):
##        w = finder_.ToolFinder('xxx', templates={'fallback_path': '%(tool)sYYY'})
##        self.assertEqual(w.fallback_path_var, 'XXXYYY')
##
##    def test__fallback_path_var__setter(self):
##        with self.assertRaises(AttributeError) as context:
##            finder_.ToolFinder('xxx').fallback_path_var = True
##        self.assertEqual(str(context.exception), "can't set attribute")

    def test__use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=True)
        self.assertTrue(w.use_vars)

    def test__use_vars__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertIsNone(w.use_vars)

    def test__use_vars__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').use_vars = True
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__use_name_var(self):
        w = finder_.ToolFinder('xxx', use_name_var=True)
        self.assertTrue(w.use_name_var)

    def test__use_name_var__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertIsNone(w.use_name_var)

    def test__use_name_var__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').use_name_var = True
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__use_priority_path_var(self):
        w = finder_.ToolFinder('xxx', use_priority_path_var=True)
        self.assertTrue(w.use_priority_path_var)

    def test__use_priority_path_var__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertIsNone(w.use_priority_path_var)

    def test__use_priority_path_var__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').use_priority_path_var = True
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__use_fallback_path_var(self):
        w = finder_.ToolFinder('xxx', use_fallback_path_var=True)
        self.assertTrue(w.use_fallback_path_var)

    def test__use_fallback_path_var__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertIsNone(w.use_fallback_path_var)

    def test__use_fallback_path_var__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').use_fallback_path_var = True
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__templates(self):
        templates = {'name' : 'N',
                     'priority_path': 'PP',
                     'fallback_path': 'FP',
                     'foo': 'FOO'}
        w = finder_.ToolFinder('xxx', templates=templates)
        expected = dict(w._default_templates, name='N', priority_path='PP', fallback_path='FP')
        self.assertEqual(w.templates, expected)

    def test__templates__default(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w.templates, w._default_templates)

    def test__templates__setter(self):
        with self.assertRaises(AttributeError) as context:
            finder_.ToolFinder('xxx').templates = '_'
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

    def test___var_for__name(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w._var_for('name'), '$XXXNAME')

    def test___var_for__name__custom_template(self):
        w = finder_.ToolFinder('xxx', templates={'name': '$%(tool)sYYY'})
        self.assertEqual(w._var_for('name'), '$xxxYYY')

    def test___var_for__priority_path(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w._var_for('priority_path'), '$XXXPRIORITYPATH')

    def test___var_for__priority_path__custom_template(self):
        w = finder_.ToolFinder('xxx', templates={'priority_path': '$%(tool)sYYY'})
        self.assertEqual(w._var_for('priority_path'), '$xxxYYY')

    def test___var_for__fallback_path(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w._var_for('fallback_path'), '$XXXFALLBACKPATH')

    def test___var_for__fallback_path__custom_template(self):
        w = finder_.ToolFinder('xxx', templates={'fallback_path': '$%(tool)sYYY'})
        self.assertEqual(w._var_for('fallback_path'), '$xxxYYY')

    def test___var_for__invalid(self):
        w = finder_.ToolFinder('xxx')
        with self.assertRaises(KeyError) as context:
            w._var_for('invalid')
        self.assertIn('invalid', str(context.exception))

    def test__default_for__name(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w._default_for('name', 'yyy'), 'yyy')

    def test__default_for__name__use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=True)
        self.assertEqual(w._default_for('name', 'yyy'), '$XXXNAME')

    def test__default_for__name__use_name_var(self):
        w = finder_.ToolFinder('xxx', use_name_var=True)
        self.assertEqual(w._default_for('name', 'yyy'), '$XXXNAME')

    def test__default_for__priority_path(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w._default_for('priority_path', []), [])

    def test__default_for__priority_path__use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=True)
        self.assertEqual(w._default_for('priority_path', []), '$XXXPRIORITYPATH')

    def test__default_for__priority_path__use_priority_path_var(self):
        w = finder_.ToolFinder('xxx', use_priority_path_var=True)
        self.assertEqual(w._default_for('priority_path', []), '$XXXPRIORITYPATH')

    def test__default_for__fallback_path(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w._default_for('fallback_path', []), [])

    def test__default_for__fallback_path__use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=True)
        self.assertEqual(w._default_for('fallback_path', []), '$XXXFALLBACKPATH')

    def test__default_for__fallback_path__use_fallback_path_var(self):
        w = finder_.ToolFinder('xxx', use_fallback_path_var=True)
        self.assertEqual(w._default_for('fallback_path', []), '$XXXFALLBACKPATH')

    def test__default_for__invalid(self):
        w = finder_.ToolFinder('xxx')
        self.assertEqual(w._default_for('invalid', 'fallback'), 'fallback')

    def test__default_for__invalid__use_vars(self):
        w = finder_.ToolFinder('xxx', use_vars=True)
        with self.assertRaises(KeyError) as context:
            w._default_for('invalid', 'fallback')
        self.assertIn('invalid', str(context.exception))

    def _whereis_1(self, prog, path, pathext, reject):
        files = [ '/opt/bin/python', '/opt/bin/xyz',
                  '/usr/bin/gcc', '/usr/bin/python',
                  '/some/where/python', '/some/where/puppet']
        if path is None:
            path = '/usr/local/bin:/usr/bin'
        if isinstance(path, str):
            path = path.split(':')
        for dir in path:
            full = '/'.join([dir, prog])
            if full in files:
                return full
        return None

    def _subst_1(self, s):
        return s

    def _env_1(self):
        return mock.Mock(WhereIs=mock.Mock(side_effect=self._whereis_1),
                         subst=mock.Mock(side_effect=self._subst_1))

    def test__adjust_result(self):
        env = self._env_1()

        find = finder_.ToolFinder('gcc')
        self.assertEqual(find._adjust_result(env, '/usr/bin/gcc', 'path'), 'gcc')

        find = finder_.ToolFinder('gcc', strip_path=False)
        self.assertEqual(find._adjust_result(env, '/usr/bin/gcc', 'path'), '/usr/bin/gcc')

    def test__adjust_result__extra_paths(self):
        env = self._env_1()

        pp = '/opt/local/bin:/opt/bin'
        fp = '/some/local/where:/some/where'

        find = finder_.ToolFinder('python', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._adjust_result(env, '/opt/bin/python', 'priority_path'), '/opt/bin/python')
        self.assertEqual(find._adjust_result(env, '/usr/bin/python', 'path'), 'python')
        self.assertEqual(find._adjust_result(env, '/some/where/python', 'fallback_path'), '/some/where/python')

        find = finder_.ToolFinder('python', priority_path=pp, strip_path=False,
                                  strip_priority_path=True, strip_fallback_path=True)
        self.assertEqual(find._adjust_result(env, '/opt/bin/python', 'priority_path'), 'python')
        self.assertEqual(find._adjust_result(env, '/usr/bin/python', 'path'), '/usr/bin/python')
        self.assertEqual(find._adjust_result(env, '/some/where/python', 'fallback_path'), 'python')

    def test__adjust_result__absname__strip(self):
        env = self._env_1()

        find = finder_.ToolFinder('python', name='/foo/bar/python', strip_path=True,
                                  strip_priority_path=True, strip_fallback_path=True)
        # absolute path given as *name* is over the strip_* settings
        self.assertEqual(find._adjust_result(env, '/opt/bin/python', 'priority_path'), '/foo/bar/python')
        self.assertEqual(find._adjust_result(env, '/usr/bin/python', 'path'), '/foo/bar/python')
        self.assertEqual(find._adjust_result(env, '/some/where/python', 'fallback_path'), '/foo/bar/python')

    def test__search(self):
        env = self._env_1()

        pp = '/opt/local/bin:/opt/bin'
        fp = '/some/local/where:/some/where'

        find = finder_.ToolFinder('python', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._search(env, 'priority_path'), '/opt/bin/python')
        self.assertEqual(find._search(env, 'path'), 'python')
        self.assertEqual(find._search(env, 'fallback_path'), '/some/where/python')

        find = finder_.ToolFinder('python', priority_path=pp, fallback_path=fp, strip_path=False,
                                  strip_priority_path=True, strip_fallback_path=True)
        self.assertEqual(find._search(env, 'priority_path'), 'python')
        self.assertEqual(find._search(env, 'path'), '/usr/bin/python')
        self.assertEqual(find._search(env, 'fallback_path'), 'python')

    def test__apply(self):
        env = self._env_1()

        pp = '/opt/local/bin:/opt/bin'
        fp = '/some/local/where:/some/where'

        find = finder_.ToolFinder('python', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._apply(env), '/opt/bin/python')

        find = finder_.ToolFinder('gcc', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._apply(env), 'gcc')

        find = finder_.ToolFinder('gcc', strip_path=False, priority_path=pp, fallback_path=fp)
        self.assertEqual(find._apply(env), '/usr/bin/gcc')

        find = finder_.ToolFinder('puppet', priority_path=pp, fallback_path=fp)
        self.assertEqual(find._apply(env), '/some/where/puppet')

        find = finder_.ToolFinder('puppet', strip_fallback_path=True, priority_path=pp, fallback_path=fp)
        self.assertEqual(find._apply(env), 'puppet')

        find = finder_.ToolFinder('inexistent')
        self.assertIsNone(find._apply(env))

    def test__call(self):
        env = self._env_1()
        # We've already tested _apply...
        with mock.patch.object(finder_.ToolFinder, '_apply', return_value='ok') as _apply:
            find = finder_.ToolFinder('foo')
            self.assertEqual(find(env), 'ok')
            _apply.assert_called_once_with(env)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

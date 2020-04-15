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

import sconstool.util.replacements_ as replacements_

class _Environment(dict):
    def SetDefault(self, **kw):
        [self.__setitem__(k, v) for k, v in kw.items() if k not in self]
    def Replace(self, **kw):
        [self.__setitem__(k, v) for k, v in kw.items()]
    def Append(self, **kw):
        pass
    def AppendUnique(self, **kw):
        pass
    def Prepend(self, **kw):
        pass
    def PrependUnique(self, **kw):
        pass
    def Override(self, overrides):
        return _Environment(self, **overrides)


class _scons_env_settersTests(unittest.TestCase):
    def test__scons_env_setters(self):
        self.assertEqual(replacements_._scons_env_setters, ('SetDefault',
                                                            'Replace',
                                                            'Append',
                                                            'AppendUnique',
                                                            'Prepend',
                                                            'PrependUnique'))

class _is_scons_envTests(unittest.TestCase):
    def test__false(self):
        incomplete = mock.Mock(SetDefault='SetDefault', spec=True)
        self.assertFalse(replacements_._is_scons_env(None))
        self.assertFalse(replacements_._is_scons_env('x'))
        self.assertFalse(replacements_._is_scons_env(incomplete))

    def test__true(self):
        env = mock.Mock(SetDefault='SetDefault',
                        Replace='Replace',
                        Append='Append',
                        AppendUnique='AppendUnique',
                        Prepend='Prepend',
                        PrependUnique='PrependUnique',
                        spec=True)
        self.assertTrue(replacements_._is_scons_env(env))
        self.assertTrue(replacements_._is_scons_env(_Environment()))


class _method_and_nameTests(unittest.TestCase):
    def test__str_attr(self):
        class Obj:
            def foo(self): pass
        obj = Obj()
        self.assertEqual(replacements_._method_and_name(obj, 'foo'), (obj.foo, 'foo'))

    def test__attr(self):
        class Obj:
            def foo(self): pass
        obj = Obj()
        self.assertEqual(replacements_._method_and_name(obj, obj.foo), (obj.foo, 'foo'))


class ReplacementsTests(unittest.TestCase):
    def test__subclass_of_dict(self):
        self.assertTrue(issubclass(replacements_.Replacements, dict))

    def test__init__(self):
        dict_ = {'a': 'A'}
        self.assertEqual(replacements_.Replacements(), dict())
        self.assertEqual(replacements_.Replacements(dict_), dict_)
        self.assertIsNot(replacements_.Replacements(dict_), dict_)
        self.assertEqual(replacements_.Replacements(dict_, b='B'), {'a': 'A', 'b': 'B'})

    def test__mapped_variables__without_arg(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        self.assertEqual(repl.mapped_variables(), {'MY_FOO': '$FOO', 'MY_BAR': '$BAR'})

    def test__mapped_variables__with_arg(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        self.assertEqual(repl.mapped_variables(['BAR']), {'MY_BAR': '$BAR'})
        self.assertEqual(repl.mapped_variables({'BAR': 'Bleah'}), {'MY_BAR': '$BAR'})

    def test__inject__1(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = dict()
        self.assertIsNone(repl.inject(dest))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'MY_BAR': '$BAR'})

    def test__inject__2(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = {'GEEZ': 'GEEZ VALUE'}
        self.assertIsNone(repl.inject(dest))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'MY_BAR': '$BAR', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__str_setter__1(self):
        class _Dict(dict):
            def my_setitem(self, key, val):
                self.__setitem__(key, val)

        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Dict({'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, 'my_setitem'))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'MY_BAR': '$BAR', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__str_setter__2(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'xxx', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, 'Replace'))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'MY_BAR': '$BAR', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__str_setter__3(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'xxx', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, 'SetDefault'))
        self.assertEqual(dest, {'MY_FOO': 'xxx', 'MY_BAR': '$BAR', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__fcn_setter__1(self):
        class _Dict(dict):
            def my_setitem(self, key, val):
                self.__setitem__(key, val)
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Dict({'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, dest.my_setitem))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'MY_BAR': '$BAR', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__fcn_setter__2(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'xxx', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, dest.SetDefault))
        self.assertEqual(dest, {'MY_FOO': 'xxx', 'MY_BAR': '$BAR', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__only_present_false__1(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = dict()
        self.assertIsNone(repl.inject(dest, only_present=False))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'MY_BAR': '$BAR'})

    def test__inject__only_present_false__1(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = {'GEEZ': 'GEEZ VALUE'}
        self.assertIsNone(repl.inject(dest, only_present=False))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'MY_BAR': '$BAR', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__only_present_true__1(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = {'GEEZ': 'GEEZ VALUE'}
        self.assertIsNone(repl.inject(dest, only_present=True))
        self.assertEqual(dest, {'GEEZ': 'GEEZ VALUE'})

    def test__inject__only_present_true__1(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = {'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'}
        self.assertIsNone(repl.inject(dest, only_present=True))
        self.assertEqual(dest, {'FOO': 'FOO VALUE', 'MY_FOO': '$FOO', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__str_setter__only_present_true__1(self):
        class _Dict(dict):
            def my_setitem(self, key, val):
                self.__setitem__(key, val)
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Dict({'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, 'my_setitem', True))
        self.assertEqual(dest, {'FOO': 'FOO VALUE', 'MY_FOO': '$FOO', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__str_setter__only_present_true__2(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'MY_FOO VALUE', 'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, 'SetDefault', True))
        self.assertEqual(dest, {'MY_FOO': 'MY_FOO VALUE', 'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__str_setter__only_present_true__3(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'MY_FOO VALUE', 'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, 'Replace', True))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__str_setter__only_present_true__4(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'MY_FOO VALUE', 'BAR': 'BAR VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, 'SetDefault', True))
        self.assertEqual(dest, {'MY_FOO': 'MY_FOO VALUE', 'MY_BAR': '$BAR', 'BAR': 'BAR VALUE', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__fcn_setter__only_present_true__1(self):
        class _Dict(dict):
            def my_setitem(self, key, val):
                self.__setitem__(key, val)
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Dict({'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, dest.my_setitem, True))
        self.assertEqual(dest, {'FOO': 'FOO VALUE', 'MY_FOO': '$FOO', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__fcn_setter__only_present_true__1(self):
        class _Dict(dict):
            def my_setitem(self, key, val):
                self.__setitem__(key, val)
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Dict({'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, 'my_setitem', True))
        self.assertEqual(dest, {'FOO': 'FOO VALUE', 'MY_FOO': '$FOO', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__fcn_setter__only_present_true__2(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'MY_FOO VALUE', 'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, dest.SetDefault, True))
        self.assertEqual(dest, {'MY_FOO': 'MY_FOO VALUE', 'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__fcn_setter__only_present_true__3(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'MY_FOO VALUE', 'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, dest.Replace, True))
        self.assertEqual(dest, {'MY_FOO': '$FOO', 'FOO': 'FOO VALUE', 'GEEZ': 'GEEZ VALUE'})

    def test__inject__fcn_setter__only_present_true__4(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        dest = _Environment({'MY_FOO': 'MY_FOO VALUE', 'BAR': 'BAR VALUE', 'GEEZ': 'GEEZ VALUE'})
        self.assertIsNone(repl.inject(dest, dest.SetDefault, True))
        self.assertEqual(dest, {'MY_FOO': 'MY_FOO VALUE', 'MY_BAR': '$BAR', 'BAR': 'BAR VALUE', 'GEEZ': 'GEEZ VALUE'})

    def test__apply(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        self.assertEqual(repl.apply(dict()), dict())
        self.assertEqual(repl.apply({'MY_FOO': '$FOO'}), dict())
        self.assertEqual(repl.apply({'MY_BAR': '$BAR'}), dict())
        self.assertEqual(repl.apply({'MY_FOO': '$FOO', 'MY_BAR': '$BAR'}), dict())
        self.assertEqual(repl.apply({'MY_FOO': 'MY_FOO VALUE'}), {'FOO': 'MY_FOO VALUE'})
        self.assertEqual(repl.apply({'MY_BAR': 'MY_BAR VALUE'}), {'BAR': 'MY_BAR VALUE'})
        self.assertEqual(repl.apply({'MY_FOO': '$FOO', 'MY_BAR': 'MY_BAR VALUE'}), {'BAR': 'MY_BAR VALUE'})
        self.assertEqual(repl.apply({'FOO': 'FOO VALUE', 'MY_BAR': 'MY_BAR VALUE'}), {'BAR': 'MY_BAR VALUE'})
        self.assertEqual(repl.apply({'GEEZ': 'GEEZ VALUE', 'MY_BAR': 'MY_BAR VALUE'}), {'BAR': 'MY_BAR VALUE'})

    def test__apply__include_unmapped(self):
        repl = replacements_.Replacements(FOO='MY_FOO', BAR='MY_BAR')
        self.assertEqual(repl.apply(dict(), True), dict())
        self.assertEqual(repl.apply({'MY_FOO': '$FOO'}, True), dict())
        self.assertEqual(repl.apply({'MY_BAR': '$BAR'}, True), dict())
        self.assertEqual(repl.apply({'MY_FOO': '$FOO', 'MY_BAR': '$BAR'}, True), dict())
        self.assertEqual(repl.apply({'MY_FOO': 'MY_FOO VALUE'}, True), {'FOO': 'MY_FOO VALUE'})
        self.assertEqual(repl.apply({'MY_BAR': 'MY_BAR VALUE'}, True), {'BAR': 'MY_BAR VALUE'})
        self.assertEqual(repl.apply({'MY_FOO': '$FOO', 'MY_BAR': 'MY_BAR VALUE'}, True), {'BAR': 'MY_BAR VALUE'})
        self.assertEqual(repl.apply({'FOO': 'FOO VALUE', 'MY_BAR': 'MY_BAR VALUE'}, True), {'FOO': 'FOO VALUE', 'BAR': 'MY_BAR VALUE'})
        self.assertEqual(repl.apply({'GEEZ': 'GEEZ VALUE', 'MY_BAR': 'MY_BAR VALUE'}, True), {'BAR': 'MY_BAR VALUE', 'GEEZ': 'GEEZ VALUE'})


class ReplacingCallerTests(unittest.TestCase):
    def test__init__1(self):
        wrapped = mock.Mock()
        wrapper = replacements_.ReplacingCaller(wrapped)
        self.assertIs(wrapper.wrapped, wrapped)
        self.assertEqual(wrapper.replacements, dict())
        self.assertIsInstance(wrapper.replacements, replacements_.Replacements)

    def test__init__2(self):
        wrapped = mock.Mock()
        wrapper = replacements_.ReplacingCaller(wrapped, {'a': 'A'}, b='B')
        self.assertIs(wrapper.wrapped, wrapped)
        self.assertEqual(wrapper.replacements, {'a': 'A', 'b': 'B'})
        self.assertIsInstance(wrapper.replacements, replacements_.Replacements)

    def test__getattr__1(self):
        foo = mock.Mock()
        wrapped = mock.Mock(foo=foo, spec=True)
        wrapper = replacements_.ReplacingCaller(wrapped)
        self.assertIs(wrapper.wrapped, wrapped)
        self.assertIs(wrapper.foo, wrapped.foo)
        with self.assertRaises(AttributeError):
            wrapper.bar

    def test__setattr__1(self):
        wrapper = replacements_.ReplacingCaller(mock.Mock())
        with self.assertRaises(AttributeError) as context:
            wrapper._wrapper_attributes = 'x'
        self.assertEqual(str(context.exception), "can't set attribute")

    def test__setattr__2(self):
        class _Wrapped(object): pass
        foo = mock.Mock()
        wrapped = _Wrapped()
        wrapper = replacements_.ReplacingCaller(wrapped)

        wrapper.replacements = 'replacements'
        wrapper.apply_replacements = 'apply_replacements'
        wrapper.inject_replacements = 'inject_replacement'
        wrapper._call = '_call'
        wrapper.sort_call_args = 'sort_call_args'
        wrapper.foo = foo

        self.assertEqual(wrapper.replacements, 'replacements')
        self.assertEqual(wrapper.apply_replacements, 'apply_replacements')
        self.assertEqual(wrapper.inject_replacements, 'inject_replacement')
        self.assertEqual(wrapper._call, '_call')
        self.assertEqual(wrapper.sort_call_args, 'sort_call_args')
        self.assertIs(wrapper.foo, foo)

        with self.assertRaises(AttributeError): wrapped.replacements
        with self.assertRaises(AttributeError): wrapped.apply_replacements
        with self.assertRaises(AttributeError): wrapped.inject_replacements
        with self.assertRaises(AttributeError): wrapped._call
        with self.assertRaises(AttributeError): wrapped.sort_call_args
        self.assertIs(wrapped.foo, foo)

    def test__apply_replacements(self):
        def apply_(*args): return 'apply%s' % repr(args)
        def Override_(*args): return 'Override%s' % repr(args)
        with mock.patch.object(replacements_.Replacements, 'apply', side_effect=apply_) as apply_mock:
            Override = mock.Mock(side_effect=Override_)
            wrapper = replacements_.ReplacingCaller('xyz')
            env = mock.Mock(Override=Override)
            expect = (Override_(apply_(env)), apply_({'a': 'A'}, True))
            self.assertEqual(wrapper.apply_replacements(env, a='A'), expect)
            apply_mock.assert_has_calls([mock.call(env), mock.call({'a': 'A'}, True)])

    def test__inject_replacements__1(self):
        with mock.patch.object(replacements_.Replacements, 'inject', return_value='Not None') as inject_mock:
            env = mock.Mock()
            wrapper = replacements_.ReplacingCaller('xyz')
            self.assertIsNone(wrapper.inject_replacements(env))
            inject_mock.assert_called_once_with(wrapper, env, '__setitem__', False)

    def test__inject_replacements_2(self):
        with mock.patch.object(replacements_.Replacements, 'inject', return_value='Not None') as inject_mock:
            env = mock.Mock()
            wrapper = replacements_.ReplacingCaller('xyz')
            self.assertIsNone(wrapper.inject_replacements(env, 'setter', 'bleah'))
            inject_mock.assert_called_once_with(wrapper, env, 'setter', 'bleah')

    def test__call(self):
        def wrapped_(*args, **kw):
            return 'wrapped(*%s, **%s)' % (repr(args), repr(kw))
        wrapped = mock.Mock(side_effect=wrapped_)
        wrapper = replacements_.ReplacingCaller(wrapped, {'FOO': 'MY_FOO', 'BAR': 'MY_BAR'})
        env = _Environment(FOO='FOO VALUE', MY_FOO='MY_FOO VALUE')
        ovr = _Environment(FOO='MY_FOO VALUE', MY_FOO='MY_FOO VALUE')
        self.assertEqual(wrapper._call(env), wrapped_(ovr))
        wrapped.assert_called_once_with(ovr)

    def test__call__args__kw(self):
        def wrapped_(*args, **kw):
            return 'wrapped(*%s, **%s)' % (repr(args), repr(kw))
        wrapped = mock.Mock(side_effect=wrapped_)
        wrapper = replacements_.ReplacingCaller(wrapped, {'FOO': 'MY_FOO', 'BAR': 'MY_BAR'})
        env = _Environment(FOO='FOO VALUE', MY_FOO='MY_FOO VALUE')
        ovr = _Environment(FOO='MY_FOO VALUE', MY_FOO='MY_FOO VALUE')
        self.assertEqual(wrapper._call(env, 'a', MY_FOO='MY_FOO VAL2'), wrapped_(ovr, 'a', FOO='MY_FOO VAL2'))
        wrapped.assert_called_once_with(ovr, 'a', FOO='MY_FOO VAL2')

    def test__inject_replacements__1(self):
        with mock.patch.object(replacements_.Replacements, 'inject', return_value='Not None') as inject_mock:
            wrapper = replacements_.ReplacingCaller('xyz', {'FOO': 'MY_FOO', 'BAR': 'MY_BAR'})
            env = mock.Mock(spec=True)
            self.assertIsNone(wrapper.inject_replacements(env))
            inject_mock.assert_called_once_with(wrapper, env, '__setitem__', False)

    def test__inject_replacements__2(self):
        with mock.patch.object(replacements_.Replacements, 'inject', return_value='Not None') as inject_mock:
            wrapper = replacements_.ReplacingCaller('xyz', {'FOO': 'MY_FOO', 'BAR': 'MY_BAR'})
            env = mock.Mock(spec=True)
            self.assertIsNone(wrapper.inject_replacements(env, 'setter', 'bleah'))
            inject_mock.assert_called_once_with(wrapper, env, 'setter', 'bleah')

    def test__sort_call_args(self):
        wrapper = replacements_.ReplacingCaller('xyz')
        self.assertEqual(wrapper.sort_call_args('a', 'b', 'c'), ('a', 'b', 'c'))


class ReplacingBuilderTests(unittest.TestCase):
    def test__call__1(self):
        def wrapped_(*args, **kw):
            return 'wrapped(*%s, **%s)' % (repr(args), repr(kw))
        wrapped = mock.Mock(side_effect=wrapped_)
        wrapper = replacements_.ReplacingBuilder(wrapped, {'FOO': 'MY_FOO', 'BAR': 'MY_BAR'})
        env = _Environment(FOO='FOO VALUE', MY_FOO='MY_FOO VALUE')
        ovr = _Environment(FOO='MY_FOO VALUE', MY_FOO='MY_FOO VALUE')
        self.assertEqual(wrapper(env, 'target', 'source'), wrapped_(ovr, 'target', 'source'))
        wrapped.assert_called_once_with(ovr, 'target', 'source')

    def test__call__2(self):
        def wrapped_(*args, **kw):
            return 'wrapped(*%s, **%s)' % (repr(args), repr(kw))
        wrapped = mock.Mock(side_effect=wrapped_)
        wrapper = replacements_.ReplacingBuilder(wrapped, {'FOO': 'MY_FOO', 'BAR': 'MY_BAR'})
        env = _Environment(FOO='FOO VALUE', MY_FOO='MY_FOO VALUE')
        ovr = _Environment(FOO='MY_FOO VALUE', MY_FOO='MY_FOO VALUE')
        self.assertEqual(wrapper(env, 'target', 'source', MY_FOO='MY_FOO VAL2'), wrapped_(ovr, 'target', 'source', FOO='MY_FOO VAL2'))
        wrapped.assert_called_once_with(ovr, 'target', 'source', FOO='MY_FOO VAL2')


class ReplacingActionTests(unittest.TestCase):
    def test__call__1(self):
        def wrapped_(*args, **kw):
            return 'wrapped(*%s, **%s)' % (repr(args), repr(kw))
        wrapped = mock.Mock(side_effect=wrapped_)
        wrapper = replacements_.ReplacingAction(wrapped, {'FOO': 'MY_FOO', 'BAR': 'MY_BAR'})
        env = _Environment(FOO='FOO VALUE', MY_FOO='MY_FOO VALUE')
        ovr = _Environment(FOO='MY_FOO VALUE', MY_FOO='MY_FOO VALUE')
        self.assertEqual(wrapper('target', 'source', env), wrapped_('target', 'source', ovr))
        wrapped.assert_called_once_with('target', 'source', ovr)

    def test__call__2(self):
        def wrapped_(*args, **kw):
            return 'wrapped(*%s, **%s)' % (repr(args), repr(kw))
        wrapped = mock.Mock(side_effect=wrapped_)
        wrapper = replacements_.ReplacingAction(wrapped, {'FOO': 'MY_FOO', 'BAR': 'MY_BAR'})
        env = _Environment(FOO='FOO VALUE', MY_FOO='MY_FOO VALUE')
        ovr = _Environment(FOO='MY_FOO VALUE', MY_FOO='MY_FOO VALUE')
        self.assertEqual(wrapper('target', 'source', ovr, MY_FOO='MY_FOO VAL2'), wrapped_('target', 'source', ovr, FOO='MY_FOO VAL2'))
        wrapped.assert_called_once_with('target', 'source', ovr, FOO='MY_FOO VAL2')


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

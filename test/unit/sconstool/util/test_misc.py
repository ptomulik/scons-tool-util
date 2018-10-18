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
import sconstool.util.misc_ as misc_

class add_dict_property_ro_Tests(unittest.TestCase):
    def test_with_attr_only(self):
        class X:
            def __init__(self, **kw):
                self._kw = kw
        misc_.add_dict_property_ro(X, '_kw', 'foo')
        misc_.add_dict_property_ro(X, '_kw', 'bar')

        self.assertTrue(hasattr(X,'foo'))
        self.assertTrue(hasattr(X,'bar'))
        self.assertIsNone(X.__doc__)

        x = X()
        self.assertIsNone(x.foo)
        self.assertIsNone(x.bar)

        x = X(foo='FOO', bar='BAR')
        self.assertEqual(x.foo, 'FOO')
        self.assertEqual(x.bar, 'BAR')

    def test_with_attr_key(self):
        class X:
            def __init__(self, **kw):
                self._kw = kw
        misc_.add_dict_property_ro(X, '_kw', ('foo', '_foo'))
        misc_.add_dict_property_ro(X, '_kw', ('bar', '_bar'))

        self.assertTrue(hasattr(X,'foo'))
        self.assertTrue(hasattr(X,'bar'))
        self.assertIsNone(X.__doc__)

        x = X()
        self.assertIsNone(x.foo)
        self.assertIsNone(x.bar)

        x = X(_foo='FOO', _bar='BAR')
        self.assertEqual(x.foo, 'FOO')
        self.assertEqual(x.bar, 'BAR')

    def test_with_doc(self):
        class X:
            def __init__(self, **kw):
                self._kw = kw
        misc_.add_dict_property_ro(X, '_kw', 'foo', doc="Returns %(attr)s or %(default)r")
        misc_.add_dict_property_ro(X, '_kw', 'bar', 'missing', doc="Returns %(attr)s or %(default)r")

        self.assertEqual(X.foo.__doc__, "Returns foo or None")
        self.assertEqual(X.bar.__doc__, "Returns bar or %r" % 'missing')

class ensure_kwarg_in_Tests(unittest.TestCase):
    def test_success(self):
        def abgen(): yield 'a'; yield 'b' # generator
        #
        self.assertTrue(misc_.ensure_kwarg_in('func()', 'a', ('a', 'b')))
        self.assertTrue(misc_.ensure_kwarg_in('func()', 'b', ('a', 'b')))
        #
        self.assertTrue(misc_.ensure_kwarg_in('func()', 'a', ['a', 'b']))
        self.assertTrue(misc_.ensure_kwarg_in('func()', 'b', ['a', 'b']))
        #
        self.assertTrue(misc_.ensure_kwarg_in('func()', 'a', {'a':'A', 'b':'B'}))
        self.assertTrue(misc_.ensure_kwarg_in('func()', 'b', {'a':'A', 'b':'B'}))
        #
        self.assertTrue(misc_.ensure_kwarg_in('func()', 'a', abgen()))
        self.assertTrue(misc_.ensure_kwarg_in('func()', 'b', abgen()))

    def test_failure(self):
        def abgen(): yield 'a'; yield 'b' # generator
        with self.assertRaises(TypeError) as context:
            misc_.ensure_kwarg_in('func()', 'c', ('a', 'b'))
        msg = "%s got an unexpected keyword argument %r" % ('func()', 'c')
        self.assertEqual(str(context.exception), msg)
        #
        with self.assertRaises(TypeError) as context:
            misc_.ensure_kwarg_in('func()', 'c', ['a', 'b'])
        msg = "%s got an unexpected keyword argument %r" % ('func()', 'c')
        self.assertEqual(str(context.exception), msg)
        #
        with self.assertRaises(TypeError) as context:
            misc_.ensure_kwarg_in('func()', 'c', {'a':'A', 'b':'A'})
        msg = "%s got an unexpected keyword argument %r" % ('func()', 'c')
        self.assertEqual(str(context.exception), msg)
        #
        with self.assertRaises(TypeError) as context:
            misc_.ensure_kwarg_in('func()', 'c', abgen())
        msg = "%s got an unexpected keyword argument %r" % ('func()', 'c')
        self.assertEqual(str(context.exception), msg)


class ensure_kwarg_not_in_Tests(unittest.TestCase):
    def test_success(self):
        def abgen(): yield 'a'; yield 'b' # generator
        self.assertTrue(misc_.ensure_kwarg_not_in('func()', 'c', ('a', 'b')))
        self.assertTrue(misc_.ensure_kwarg_not_in('func()', 'c', ['a', 'b']))
        self.assertTrue(misc_.ensure_kwarg_not_in('func()', 'c', {'a':'A', 'b':'B'}))
        self.assertTrue(misc_.ensure_kwarg_not_in('func()', 'c', abgen()))

    def test_failure(self):
        def abgen(): yield 'a'; yield 'b' # generator
        with self.assertRaises(TypeError) as context:
            misc_.ensure_kwarg_not_in('func()', 'b', ('a', 'b'))
        msg = "%s got a forbidden keyword argument %r" % ('func()', 'b')
        self.assertEqual(str(context.exception), msg)
        #
        with self.assertRaises(TypeError) as context:
            misc_.ensure_kwarg_not_in('func()', 'b', ['a', 'b'])
        msg = "%s got a forbidden keyword argument %r" % ('func()', 'b')
        self.assertEqual(str(context.exception), msg)
        #
        with self.assertRaises(TypeError) as context:
            misc_.ensure_kwarg_not_in('func()', 'b', {'a':'A', 'b':'B'})
        msg = "%s got a forbidden keyword argument %r" % ('func()', 'b')
        self.assertEqual(str(context.exception), msg)
        #
        with self.assertRaises(TypeError) as context:
            misc_.ensure_kwarg_not_in('func()', 'b', abgen())
        msg = "%s got a forbidden keyword argument %r" % ('func()', 'b')
        self.assertEqual(str(context.exception), msg)


class check_kwarg_Tests(unittest.TestCase):
    def test_calls(self):
        fcn = lambda s : 'sconstool.util.misc_.ensure_kwarg_%s' % s
        with mock.patch(fcn('in')) as check_in, \
             mock.patch(fcn('not_in')) as check_not_in:
            self.assertTrue(misc_.check_kwarg('func()', 'foo', 'allowed', 'forbidden'))
            check_in.assert_called_once_with('func()', 'foo', 'allowed')
            check_not_in.assert_called_once_with('func()', 'foo', 'forbidden')


class check_kwargs_Tests(unittest.TestCase):
    def test_calls(self):
        with mock.patch('sconstool.util.misc_.check_kwarg') as check_key:
            self.assertTrue(misc_.check_kwargs('func()', ('k1', 'k2'), 'allowed', 'forbidden'))
            check_key.assert_has_calls([mock.call('func()','k1','allowed','forbidden'),
                                        mock.call('func()','k2','allowed','forbidden')])


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

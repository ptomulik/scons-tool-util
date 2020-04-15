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
if sys.version_info < (3,0):
    import unittest2 as unittest
    import mock
else:
    import unittest
    import unittest.mock as mock
import sconstool.util.emitter_ as emitter_


class _Node(object):
    def __init__(self, path):
        self.path = path
    def __str__(self):
        return str(self.path)


class ConditionalEmitterTests(unittest.TestCase):

    def test__init__predicate_not_callable(self):
        with self.assertRaises(TypeError) as context:
            emitter_.ConditionalEmitter('predicate')
        self.assertEqual(str(context.exception), "predicate must be callable")

    def test__init__(self):
        def pred(): pass
        em = emitter_.ConditionalEmitter(pred)
        self.assertIs(em.predicate, pred)
        self.assertIs(em.emitter_if.__code__, em.default_emitter.__code__)
        self.assertIs(em.emitter_else.__code__, em.default_emitter.__code__)

    def test__default_emitter(self):
        def pred(): pass
        em = emitter_.ConditionalEmitter(pred)
        target = mock.Mock()
        source = mock.Mock()
        env = mock.Mock()
        (t, s) = em.default_emitter(target, source, env)
        self.assertIs(t, target)
        self.assertIs(s, source)

    def test__call__(self):
        def src_suffix_in(target, source, env):
            return str(source[0]).endswith('.in')
        def suffix_out(target, source, env):
            return str(target[0]).endswith('.out')

        env = mock.Mock()
        file_out = [_Node('file.out')]
        file_in = [_Node('file.in')]
        file_xx = [_Node('file.xx')]

        em_if = mock.Mock(return_value='emitter_if')
        em_else = mock.Mock(return_value='emitter_else')
        em = emitter_.ConditionalEmitter(src_suffix_in, em_if, em_else)
        self.assertEqual(em(file_out, file_in, env), 'emitter_if')
        em_if.assert_called_once_with(file_out, file_in, env)
        em_else.assert_not_called()

        em_if = mock.Mock(return_value='emitter_if')
        em_else = mock.Mock(return_value='emitter_else')
        em = emitter_.ConditionalEmitter(src_suffix_in, em_if, em_else)
        self.assertEqual(em(file_out, file_xx, env), 'emitter_else')
        em_if.assert_not_called()
        em_else.assert_called_once_with(file_out, file_xx, env)

        em_if = mock.Mock(return_value='emitter_if')
        em_else = mock.Mock(return_value='emitter_else')
        em = emitter_.ConditionalEmitter(suffix_out, em_if, em_else)
        self.assertEqual(em(file_out, file_in, env), 'emitter_if')
        em_if.assert_called_once_with(file_out, file_in, env)
        em_else.assert_not_called()

        em_if = mock.Mock(return_value='emitter_if')
        em_else = mock.Mock(return_value='emitter_else')
        em = emitter_.ConditionalEmitter(suffix_out, em_if, em_else)
        self.assertEqual(em(file_xx, file_in, env), 'emitter_else')
        em_if.assert_not_called()
        em_else.assert_called_once_with(file_xx, file_in, env)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import types

import sconstool.util.imports_ as imports_

try:
    from . import pkg
    from .pkg import src1
    from .pkg import src2
    from .pkg import tgt1
    from .pkg import tgt2
    from .pkg import tgt3
except ImportError:
    import pkg
    import pkg.src1
    import pkg.src2
    import pkg.tgt1
    import pkg.tgt2
    import pkg.tgt3

class Test__Imports(unittest.TestCase):
    def test__all_symbols__1(self):
        symbols = imports_.all_symbols(pkg.src1)
        self.assertIn('foo1', symbols)
        self.assertIn('bar1', symbols)
        self.assertIn('geez1', symbols)

    def test__all_symbols__2(self):
        symbols = imports_.all_symbols(pkg.src2)
        self.assertIn('foo2', symbols)
        self.assertIn('bar2', symbols)
        self.assertNotIn('geez2', symbols)

    def test__import_from__1(self):
        class T: pass
        imports_.import_from(T, pkg.src1, ('foo1',))
        self.assertIs(T.foo1, pkg.src1.foo1)
        self.assertFalse(hasattr(T, 'bar1'))
        self.assertFalse(hasattr(T, 'geez1'))

    def test__import_from__2(self):
        class T: pass
        imports_.import_from(T, pkg.src2, ('foo2', 'bar2', 'geez2'))
        self.assertIs(T.foo2, pkg.src2.foo2)
        self.assertIs(T.bar2, pkg.src2.bar2)
        self.assertIs(T.geez2, pkg.src2.geez2)

    def test__import_all_from__1(self):
        class T: pass
        imports_.import_all_from(T, pkg.src1)
        self.assertIs(T.foo1, pkg.src1.foo1)
        self.assertIs(T.bar1, pkg.src1.bar1)
        self.assertIs(T.geez1, pkg.src1.geez1)

    def test__import_all_from__2(self):
        class T: pass
        imports_.import_all_from(T, pkg.src2)
        self.assertIs(T.foo2, pkg.src2.foo2)
        self.assertIs(T.bar2, pkg.src2.bar2)
        self.assertFalse(hasattr(T,'geez2'))

    def test__import_all_from__3(self):
        class T: pass
        imports_.import_all_from(T, (pkg.src1, pkg.src2))
        self.assertIs(T.foo1, pkg.src1.foo1)
        self.assertIs(T.bar1, pkg.src1.bar1)
        self.assertIs(T.geez1, pkg.src1.geez1)
        self.assertIs(T.foo2, pkg.src2.foo2)
        self.assertIs(T.bar2, pkg.src2.bar2)
        self.assertFalse(hasattr(T,'geez2'))

    def test__import_all_from__4(self):
        imports_.import_all_from(pkg.tgt1, ('.src3', '.src4'), pkg.__name__)
        self.assertIs(pkg.tgt1.foo3, pkg.src3.foo3)
        self.assertIs(pkg.tgt1.bar3, pkg.src3.bar3)
        self.assertIs(pkg.tgt1.geez3, pkg.src3.geez3)
        self.assertIs(pkg.tgt1.foo4, pkg.src4.foo4)
        self.assertIs(pkg.tgt1.bar4, pkg.src4.bar4)
        self.assertFalse(hasattr(pkg.tgt1,'geez4'))

    def test__import_all_from__5(self):
        self.assertIs(pkg.tgt2.foo5, pkg.src5.foo5)
        self.assertIs(pkg.tgt2.bar5, pkg.src5.bar5)
        self.assertFalse(hasattr(pkg.tgt2,'geez5'))

    def test__import_all_from__6(self):
        self.assertIs(pkg.tgt3.foo5, pkg.src5.foo5)
        self.assertIs(pkg.tgt3.bar5, pkg.src5.bar5)
        self.assertFalse(hasattr(pkg.tgt3,'geez5'))


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:

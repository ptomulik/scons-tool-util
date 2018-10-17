# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Pawel Tomulik
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
import sconstool.util as util
import sconstool.util.misc_ as misc_
import sconstool.util.finder_ as finder_


class package_symbols_Tests(unittest.TestCase):
    def test_misc_(self):
        self.assertIs(util.add_dict_property_ro, misc_.add_dict_property_ro)
        self.assertIs(util.ensure_kwarg_in, misc_.ensure_kwarg_in)
        self.assertIs(util.ensure_kwarg_not_in, misc_.ensure_kwarg_not_in)
        self.assertIs(util.check_kwarg, misc_.check_kwarg)
        self.assertIs(util.check_kwargs, misc_.check_kwargs)

    def test_finder_(self):
        self.assertIs(util.ToolFinder, finder_.ToolFinder)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
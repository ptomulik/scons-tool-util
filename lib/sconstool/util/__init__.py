# -*- coding: utf-8 -*-
"""Top-level module."""

from .about import __version__

from .imports_ import *

__all__ = imports_.__all__

import_all_from(__package__, [
    '.misc_',
    '.finder_',
    '.emitter_',
    '.selector_',
    '.replacements_'
])

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:

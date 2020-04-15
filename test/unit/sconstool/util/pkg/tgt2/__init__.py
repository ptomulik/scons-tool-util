# -*- coding: utf-8 -*-

import sys
from sconstool.util import import_all_from
parent = '.'.join(__package__.split('.')[0:-1])
import_all_from(sys.modules[__package__], '.src5', parent)

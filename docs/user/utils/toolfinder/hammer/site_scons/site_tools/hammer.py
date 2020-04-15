# -*- coding: utf-8 -*-
from sconstool.util import *
from SCons.Builder import Builder
import sys

_hammer = ToolFinder('hammer', name='hammer.py', pathext=['.py'], priority_path='bin')


def generate(env):
    env.SetDefault(PYTHON=sys.executable)
    env.SetDefault(HAMMER=_hammer(env))
    env['HAMMERCOM'] = '$PYTHON $HAMMER $TARGET $SOURCE'
    env['BUILDERS']['Hammer'] = Builder(action='$HAMMERCOM')


def exists(env):
    return _hammer(env)

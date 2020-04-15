# -*- coding: utf-8 -*-
from sconstool.util import *
from SCons.Builder import Builder

_iconv = ToolFinder('iconv')


def generate(env):
    env.SetDefault(ICONVFROM='UTF-8', ICONVTO='UTF-8')
    env.SetDefault(ICONV=_iconv(env))
    env['ICONVCOM'] = '$ICONV -f $ICONVFROM -t $ICONVTO $SOURCE > $TARGET'
    env['BUILDERS']['Iconv'] = Builder(action='$ICONVCOM')


def exists(env):
    return _iconv(env)

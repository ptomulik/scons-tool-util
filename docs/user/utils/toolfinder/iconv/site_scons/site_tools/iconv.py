from sconstool.util import *
from SCons.Builder import Builder

_iconv = ToolFinder('iconv')


def generate(env):
    env.SetDefault(ICONVFROM='utf8', ICONVTO='utf8')
    env.SetDefault(ICONV=_iconv(env))
    env['ICONVCOM'] = '$ICONV -f $ICONVFROM -t $ICONVTO $SOURCE > $TARGET'
    env['BUILDERS']['Iconv'] = Builder(action='$ICONVCOM')


def exists(env):
    return _iconv(env)

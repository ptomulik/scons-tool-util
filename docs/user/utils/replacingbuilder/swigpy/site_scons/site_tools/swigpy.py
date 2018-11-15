from sconstool.util import *
import SCons.Tool
import SCons.Builder

SwigPyVars = [
  'LINK',
  'LINKFLAGS',
  'LIBPATH',
  'LIBS',
  'SHOBJPREFIX',
  'SHOBJSUFFIX',
  'LIBPREFIX',
  'LIBSUFFIX',
  'SHLIBPREFIX',
  'SHLIBSUFFIX',
  'IMPLIBPREFIX',
  'IMPLIBSUFFIX',
  'WINDOWSEXPPREFIX',
  'WINDOWSEXPSUFFIX'
]


SwigPyReplacements = Replacements({k: 'SWIGPY_%s' % k for k in SwigPyVars })


class SwigPyShlibBuilder(ReplacingBuilder):
    def __call__(self, env, target, source, **kw):
        # preserve original 'LIBSUFFIXES' and 'LIBPREFIXES', such that
        # libraries having original 'LIBPREFIX', 'LIBSUFFIX', 'SHLIBPREFIX',
        # etc. will be found when required by the linker.
        ovr = {'LIBPREFIXES': [env.subst(x) for x in env['LIBPREFIXES']],
               'LIBSUFFIXES': [env.subst(x) for x in env['LIBSUFFIXES']]}
        return ReplacingBuilder.__call__(self, env, target, source, **dict(ovr, **kw))


def createSwigPyShlibBuilder(env):
    try:
        swigpy_shlib = env['BUILDERS']['SwigPyShlib']
    except KeyError:
        shlib = SCons.Tool.createSharedLibBuilder(env)
        swigpy_shlib = SwigPyShlibBuilder(shlib, SwigPyReplacements)
        env['BUILDERS']['SwigPyShlib'] = swigpy_shlib
    return swigpy_shlib


def setSwigPyDefaults(env):
    env.SetDefault(SWIGPY_SHLIBPREFIX='_')
    env.SetDefault(SWIGPY_LIBPREFIX='_')
    env.SetDefault(SWIGPY_IMPLIBPREFIX='_')
    env.SetDefault(SWIGPY_WINDOWSEXPPREFIX='_')
    env.SetDefault(SWIGPY_SHLIBSUFFIX='.pyd')
    SwigPyReplacements.inject(env, 'SetDefault')


def generate(env):
    createSwigPyShlibBuilder(env)
    setSwigPyDefaults(env)


def exists(env):
    return 1

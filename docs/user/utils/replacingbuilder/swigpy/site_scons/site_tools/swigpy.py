from sconstool.util import *
import SCons.Tool
import SCons.Builder

swigPyReplacements = {
  'LINK': 'SWIGPY_LINK',
  'LINKFLAGS': 'SWIGPY_LINKFLAGS',
  'LIBPATH': 'SWIGPY_LIBPATH',
  'LIBS': 'SWIGPY_LIBS',
  'SHOBJPREFIX': 'SWIGPY_SHOBJPREFIX',
  'SHOBJSUFFIX': 'SWIGPY_SHOBJSUFFIX',
  'LIBPREFIX': 'SWIGPY_LIBPREFIX',
  'LIBSUFFIX': 'SWIGPY_LIBSUFFIX',
  'SHLIBPREFIX': 'SWIGPY_SHLIBPREFIX',
  'SHLIBSUFFIX': 'SWIGPY_SHLIBSUFFIX',
  'IMPLIBPREFIX': 'SWIGPY_IMPLIBPREFIX',
  'IMPLIBSUFFIX': 'SWIGPY_IMPLIBSUFFIX',
  'WINDOWSEXPPREFIX': 'SWIGPY_WINDOWSEXPPREFIX',
  'WINDOWSEXPSUFFIX': 'SWIGPY_WINDOWSEXPSUFFIX'
}


class SwigPyShlibBuilder(ReplacingBuilder):
    def __call__(self, env, target, source, **kw):
        # preserve 'LIBSUFFIXES' and 'LIBPREFIXES'
        ovr = {'LIBPREFIXES': [env.subst(x) for x in env['LIBPREFIXES']],
               'LIBSUFFIXES': [env.subst(x) for x in env['LIBSUFFIXES']]}
        return ReplacingBuilder.__call__(self, env, target, source, **dict(ovr, **kw))


def createSwigPyShlibBuilder(env):
    try:
        swigpy_shlib = env['BUILDERS']['SwigPyShlib']
    except KeyError:
        shlib = SCons.Tool.createSharedLibBuilder(env)
        swigpy_shlib = SwigPyShlibBuilder(shlib, swigPyReplacements)
        env['BUILDERS']['SwigPyShlib'] = swigpy_shlib
    return swigpy_shlib


def setSwigPyDefaults(env, replacements):
    env.SetDefault(SWIGPY_SHLIBPREFIX='_')
    env.SetDefault(SWIGPY_LIBPREFIX='_')
    env.SetDefault(SWIGPY_IMPLIBPREFIX='_')
    env.SetDefault(SWIGPY_WINDOWSEXPPREFIX='_')
    env.SetDefault(SWIGPY_SHLIBSUFFIX='.pyd')
    replacements.inject(env, 'SetDefault')


def generate(env):
    swigpy_shlib = createSwigPyShlibBuilder(env)
    setSwigPyDefaults(env, swigpy_shlib.replacements)


def exists(env):
    return 1

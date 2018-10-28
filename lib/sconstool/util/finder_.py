# -*- coding: utf-8 -*-
"""Provides the :class:`.ToolFinder` class.
"""

from . import misc_
import os


__all__ = ('ToolFinder',)


class ToolFinder(object):
    """Callable object which searches for executables.

    A single ToolFinder instance searches for a single file (program), for
    example a compiler executable or script interpreter. The constructor
    accepts several options, for each option there is corresponding
    @property (read-only) with the same name.

    :Example: Typical use in a tool module

    .. code-block:: python

        from sconstool.util import ToolFinder
        foo = ToolFinder('foo')

        def generate(env):
            env.SetDefault(FOO=foo(env))
            # ...

        def exists(env):
            return env.get('FOO', foo(env))
    """
    __slots__ = ('_tool', '_kw')

    _ctor_kwargs = ('name',
                    'path',
                    'pathext',
                    'reject',
                    'priority_path',
                    'fallback_path',
                    'strip_path',
                    'strip_priority_path',
                    'strip_fallback_path')

    def __init__(self, tool, **kw):
        """
        :param str tool:
            symbolic name of the tool,
        :keyword str,list name:
            base name of the file (program name) being searched for,
            may be a list of alternative program names,
        :keyword str,list path:
            search path to be used instead of the standard SCons PATH,
        :keyword str,list pathext:
            a list of file extensions to be considered as executable,
        :keyword list reject:
            a list of paths to be rejected,
        :keyword str,list priority_path:
            extra search path to be searched prior to :attr:`.path`,
        :keyword str,list fallback_path:
            extra search path to be searched after :attr:`.path`,
        :keyword bool strip_path:
            if ``True`` (default), the leading path, if it's in :attr:`path`
            list, will be stripped from the returned file path,
        :keyword bool strip_priority_path:
            if ``True``, the leading path, if it's in **priority_path**
            list, will be stripped from the returned file path;
        :keyword bool strip_fallback_path:
            if ``True``, the leading path, if it's in **fallback_path** list,
            will be stripped from the returned file path.
        """
        self._tool = str(tool)
        misc_.check_kwargs('ToolFinder()', kw, self._ctor_kwargs)
        self._kw = kw

    @property
    def tool(self):
        """Tool name, that was passed in to the c-tor as an argument.

           :rtype: str
        """
        return self._tool

    def __call__(self, env):
        """Performs the actual search.

           :param env:
                a SCons environment; provides construction variables and the
                ``env.WhereIs()`` method to the :class:`.ToolFinder`.
           :return:
                depending on options chosen at object creation, a name or a
                path to the executable file found. If the program can't be
                found, ``None`` is returned.
           :rtype: str
        """
        return self._search(env)

    def _whereis(self, env, prog, where):
        path = getattr(self, where)
        if path and not isinstance(path, str):
            # this trick enables variable substitution in list entries
            path = os.path.pathsep.join(path)
        return env.WhereIs(prog, path, self.pathext, self.reject)

    def _adjust_result(self, env, result, where):
        prog = env.subst(result[0])
        strip = getattr(self, 'strip_%s' % where)
        if os.path.isabs(prog) or strip:
            return prog
        return result[1]

    def _search_in(self, env, where):
        progs = self.name
        if isinstance(progs, str):
            progs = [progs]
        for prog in progs:
            found = self._whereis(env, prog, where)
            if found:
                return self._adjust_result(env, (prog, found), where)
        return None

    def _search(self, env):
        for where in ('priority_path', 'path', 'fallback_path'):
            found = self._search_in(env, where)
            if found:
                return found
        return None

    @classmethod
    def _add_getter(cls, attr, default=None, **kw):
        if isinstance(default, property):
            default = default.fget
            kw['defaultattr'] = default.__name__

            doc = """\
            The value of **%(attr)s** keyword argument passed in to the
            constructor at object creation, or ``self.%(defaultattr)s`` if the
            argument was omitted.

            :rtype: %(rtype)s
            """
        else:
            doc = """\
            The value of **%(attr)s** keyword argument passed in to the
            constructor at object creation, or ``%(default)r`` if the
            argument was omitted.

            :rtype: %(rtype)s
            """
        kw = dict({'doc': doc}, **kw)
        misc_.add_ro_dict_property(cls, '_kw', attr, default, **kw)


TF = ToolFinder
TF._add_getter('name', TF.tool, rtype='str')
TF._add_getter('path', rtype='str,list')
TF._add_getter('priority_path', [], rtype='str,list')
TF._add_getter('fallback_path', [], rtype='str,list')
TF._add_getter('pathext', rtype='str,list')
TF._add_getter('reject', [], rtype='list')
TF._add_getter('strip_path', True, rtype='bool')
TF._add_getter('strip_priority_path', False, rtype='bool')
TF._add_getter('strip_fallback_path', False, rtype='bool')
del TF


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:

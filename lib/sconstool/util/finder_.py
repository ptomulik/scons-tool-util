# -*- coding: utf8 -*-
"""Utility functions to automate (sub)module imports.
"""

from . import misc_
import os


__all__ = ('ToolFinder',)


class ToolFinder:
    """Callable object which helps searching for programs used by SCons tools.

    A single ToolFinder instance searches for a single file (program), for
    example a compiler executable or script interpreter.

    :example: Simplest use

    Suppose, you develop a tool named ``hammer``, which needs an executable
    named ``hammer``, which is expected to be found in a SCons search PATH.

    .. code-block:: python

        from sconstool.util import *
        find_hammer = ToolFinder('hammer')

        def generate(env):
            env['HAMMER'] = find_hammer(env)

        def exists(env):
            return find_hammer(env)

    The constructor accepts several options, such that the search may be
    customized.
    """
    __slots__ = ('_tool', '_kw', '_templates')

    _ctor_kwargs = ('name', 'path', 'priority_path', 'fallback_path',
                    'use_vars', 'use_name_var', 'use_priority_path_var',
                    'use_fallback_path_var', 'strip_path',
                    'strip_priority_path', 'strip_fallback_path',
                    'templates', 'var_sep')

    _default_templates = {
        'name':          '%(tool)s%(var_sep)sNAME',
        'priority_path': '%(tool)s%(var_sep)sPATH',
        'fallback_path': '%(tool)s%(var_sep)sFALLBACKPATH',
    }

    def __init__(self, tool, **kw):
        """
        :param str tool:
            symbolic name of the tool,
        :keyword str name:
            base name of the file (program name) being searched for,
        :keyword str,list path:
            search path to be used instead of the standard SCons PATH,
        :keyword str,list priority_path:
            extra search path to be searched prior to :attr:`.path`,
        :keyword str,list fallback_path:
            extra search path to be searched after :attr:`.path`,
        :keyword bool use_vars:
            use supporting construction variables to generate :attr:`.name`,
            :attr:`priority_path`, :attr:`fallback_path`,
        :keyword bool use_name_var:
            if ``True``, and **name** is not given, a supporting construction
            variable will be used to provide :attr:`.default_name`,
        :keyword bool use_priority_path_var:
            if ``True``, and **priority_path** is not given, a supporting
            construction variable will be used to provide
            :attr:`.default_priority_path`,
        :keyword bool use_fallback_path_var:
            if ``True``, and **fallback_path** is not given, a supporting
            construction variable will be used to provide
            :attr:`.default_fallback_path`,
        :keyword str var_sep:
            a separator, used by :attr:`.templates`,
        :keyword dict templates:
            a dictionary of overrides for templates used to generate names of
            the supporting construction variables,
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
        self._init_templates(kw)
        self._kw = kw

    @property
    def tool(self):
        """Tool name, that was passed in to the c-tor as an argument.

           :rtype: str
        """
        return self._tool

    @property
    def name(self):
        """Actual (base) name of the file being searched for.

           :rtype: str
        """
        return self._kw.get('name', self.default_name)

    @property
    def priority_path(self):
        """The **priority_path** keyword argument passed in to the constructor
           at object creation. If the argument was not provided,
           :attr:`.default_priority_path` is returned.

           :rtype: str,list
        """
        return self._kw.get('priority_path', self.default_priority_path)

    @property
    def fallback_path(self):
        """The **fallback_path** keyword argument passed in to the constructor
           at object creation. If the argument was not provided,
           :attr:`.default_fallback_path` is returned.

           :rtype: str,list
        """
        return self._kw.get('fallback_path', self.default_fallback_path)

    @property
    def default_name(self):
        """Default (base) name of the file being searched for.

           :rtype: str
        """
        return self._default_for('name', self.tool)

    @property
    def default_priority_path(self):
        """Default value for :attr:`.priority_path`.

           :rtype: str
        """
        return self._default_for('priority_path', [])

    @property
    def default_fallback_path(self):
        """Default value for :attr:`.fallback_path`.

           :rtype: str
        """
        return self._default_for('fallback_path', [])

    @property
    def name_var(self):
        """Name of the variable used for :attr:`.default_name`.

           :rtype: str
        """
        return self._var_for('name')

    @property
    def priority_path_var(self):
        """Name of the variable used for :attr:`.default_priority_path`.

           :rtype: str
        """
        return self._var_for('priority_path')

    @property
    def fallback_path_var(self):
        """Name of the variable used for :attr:`default_fallback_path`.

           :rtype: str
        """
        return self._var_for('fallback_path')

    @property
    def templates(self):
        """A dictionary of templates used to generate variable names for
           :attr:`.default_name`, :attr:`.default_priority_path`, and
           :attr:`.fallback_path`.

           :rtype: dict
        """
        return self._templates

    def __call__(self, env):
        """Performs the actual search.

           :param env:
                a SCons environment, for which the tool is being prepared; the
                environment provides construction variables and the
                functionality of its ``WereIs()`` method,
           :return:
                depending on options chosen (at the object construction), a
                name or a path to the file found. If file can't be found,
                ``None`` is returned.
           :rtype: str
        """
        return self._apply(env)

    def _init_templates(self, kw):
        default = self._default_templates
        target = default.copy()
        try:
            source = kw['templates']
        except KeyError:
            pass
        else:
            target.update({k: source[k] for k in source if k in default})
            del kw['templates']
        self._templates = target

    def _var_for(self, what):
        attrs = {k: getattr(self, k) for k in ('tool', 'var_sep')}
        return (self._templates[what] % attrs).upper()

    def _default_for(self, what, fallback):
        if self._kw.get('use_%s_var' % what, self._kw.get('use_vars')):
            return "$%s" % self._var_for(what)
        else:
            return fallback

    def _detect(self, env, name, path=None):
        if env.WhereIs(name, path):
            return env.subst(name)
        else:
            return None

    def _adjust_detected(self, env, detected, where):
        isabs = os.path.isabs
        normpath = os.path.normpath
        strip = getattr(self, 'strip_%s' % where)
        if isabs(detected) or strip:
            return detected
        return env.WhereIs(self.name, getattr(self, where))

    def _search(self, env, where):
        detected = self._detect(env, self.name, getattr(self, where))
        if detected:
            return self._adjust_detected(env, detected, where)
        return None

    def _apply(self, env):
        for where in ('priority_path', 'path', 'fallback_path'):
            found = self._search(env, where)
            if found:
                return found
        return None

    @classmethod
    def _add_ctor_arg_getter(cls, attr, default=None, **kw):
        doc = """\
        The value of **%(attr)s** keyword argument passed in to the constructor
        at object creation. ``%(default)r`` if the argument was omitted.

        :rtype: %(rtype)s
        """
        kw = dict({'doc': doc}, **kw)
        misc_.add_dict_property_ro(cls, '_kw', attr, default, **kw)


ToolFinder._add_ctor_arg_getter('var_sep', '', rtype='str')
ToolFinder._add_ctor_arg_getter('path', rtype='str,list')
ToolFinder._add_ctor_arg_getter('use_vars', rtype='bool')
ToolFinder._add_ctor_arg_getter('use_name_var', rtype='bool')
ToolFinder._add_ctor_arg_getter('use_priority_path_var', rtype='bool')
ToolFinder._add_ctor_arg_getter('use_fallback_path_var', rtype='bool')
ToolFinder._add_ctor_arg_getter('strip_path', True, rtype='bool')
ToolFinder._add_ctor_arg_getter('strip_priority_path', False, rtype='bool')
ToolFinder._add_ctor_arg_getter('strip_fallback_path', False, rtype='bool')

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:

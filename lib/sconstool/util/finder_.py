# -*- coding: utf-8 -*-
"""Utility functions to automate (sub)module imports.
"""

from . import misc_
import os


__all__ = ('ToolFinder',)


class ToolFinder:
    """Callable object which helps searching for programs used by SCons tools.

    A single ToolFinder instance searches for a single file (program), for
    example a compiler executable or script interpreter. The constructor
    accepts several options, for each option there is corresponding object
    property (read-only) with the same name.
    """
    __slots__ = ('_tool', '_kw', '_templates')

    _ctor_kwargs = ('name',
                    'path',
                    'pathext',
                    'reject',
                    'priority_path',
                    'fallback_path',
                    'use_vars',
                    'use_name_var',
                    'use_priority_path_var',
                    'use_fallback_path_var',
                    'strip_path',
                    'strip_priority_path',
                    'strip_fallback_path',
                    'templates')

    _default_templates = {
        'name':          '$%(TOOL)sNAME',
        'priority_path': '$%(TOOL)sPRIORITYPATH',
        'fallback_path': '$%(TOOL)sFALLBACKPATH',
    }

    def __init__(self, tool, **kw):
        """
        :param str tool:
            symbolic name of the tool,
        :keyword str name:
            base name of the file (program name) being searched for,
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
        :keyword dict templates:
            a dictionary of overrides for :attr:`.templates` used to generate
            names of the supporting construction variables,
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
    def templates(self):
        """A dictionary of templates used to generate variable names for
           :attr:`.default_name`, :attr:`.default_priority_path`, and
           :attr:`.default_fallback_path`.

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
        attrs = {k: getattr(self, k) for k in ('tool',)}
        attrs.update({k.upper(): getattr(self, k).upper() for k in ('tool',)})
        return (self._templates[what] % attrs)

    def _default_for(self, what, fallback):
        if self._kw.get('use_%s_var' % what, self._kw.get('use_vars')):
            return self._var_for(what)
        else:
            return fallback

    def _whereis(self, env, where):
        path = getattr(self, where)
        return env.WhereIs(self.name, path, self.pathext, self.reject)

    def _adjust_result(self, env, found, where):
        name = env.subst(self.name)
        strip = getattr(self, 'strip_%s' % where)
        if os.path.isabs(name) or strip:
            return name
        return found

    def _search(self, env, where):
        found = self._whereis(env, where)
        if found is None:
            return None
        return self._adjust_result(env, found, where)

    def _apply(self, env):
        for where in ('priority_path', 'path', 'fallback_path'):
            found = self._search(env, where)
            if found:
                return found
        return None

    @classmethod
    def _add_ctor_arg_getter(cls, attr, default=None, **kw):
        if kw.get('smart'):
            del kw['smart']
            if default is None:
                kw['defaultattr'] = 'default_%s' % attr
            else:
                kw['defaultattr'] = default

            def default(obj, da=kw['defaultattr']):
                return getattr(obj, da)

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


ToolFinder._add_ctor_arg_getter('name', smart=True, rtype='str')
ToolFinder._add_ctor_arg_getter('priority_path', smart=True, rtype='str,list')
ToolFinder._add_ctor_arg_getter('fallback_path', smart=True, rtype='str,list')
ToolFinder._add_ctor_arg_getter('path', rtype='str,list')
ToolFinder._add_ctor_arg_getter('pathext', rtype='str,list')
ToolFinder._add_ctor_arg_getter('reject', [], rtype='list')
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

# -*- coding: utf-8 -*-
"""Provides the :class:`.Replacements` class.
"""


__all__ = ('Replacements',
           'ReplacingCaller',
           'ReplacingBuilder',
           'ReplacingAction')


_scons_env_setters = ('SetDefault',
                      'Replace',
                      'Append',
                      'AppendUnique',
                      'Prepend',
                      'PrependUnique')


def _is_scons_env(obj):
    return all(hasattr(obj, m) for m in _scons_env_setters)


def _method_and_name(obj, method):
    if isinstance(method, str):
        name = method
        method = getattr(obj, method)
    else:
        name = method.__name__
    return (method, name)


class Replacements(dict):
    """Enables one to temporarily replace variables in a dict-like object
    (SCons ``Environment``).

    The :class:`.Replacements` are designed to be used with
    :class:`.ReplacingBuilder` or :class:`.ReplacingAction`.
    """
    def mapped_variables(self, only=None):
        if only is not None:
            return {v: '$' + k for k, v in self.items() if k in only}
        else:
            return {v: '$' + k for k, v in self.items()}

    def inject(self, dest, setter='__setitem__', only_present=False):
        """Inject replacement variables into the **dest**.

        This method is supposed to be used to initialize replacement variables
        in the dictionary **dest**. For each mapping ``{'FOO': 'BAR'}`` in
        :class:`.Replacements` ``dest['BAR'] = '$FOO'`` assignment will be
        performed using the provided **setter**. If **only_present** is
        ``True``, the assignment will be performed only if the variable
        ``dest['FOO']`` is already defined.

        :param dict dest:
            destination dictionary to be modified,
        :param str,callable setter:
            a method (or method name) of **dest** that sets items in **dest**,
            should be a function with prototype ``dest.setter(name, value)``,
            except for ``SetDefault``, ``Replace``, ``Append``, ``Prepend``,
            ``AppendUnique``, ``PrependUnique`` methods of SCons environment
            where the prototype is ``dest.setter(**kw)``,
        :param bool only_present:
            if ``True``, only the replacements for variables already present in
            **dest** will be set.
        """
        variables = self.mapped_variables(dest if only_present else None)
        self._do_inject(dest, setter, variables)

    def apply(self, subj, include_unmapped=False):
        """Apply replacements to **subj**.

        Returns a dictionary of variables from **subj** set to their
        replacement values. By default, only variables having their
        replacements are extracted. If **include_unmapped** is ``True``,
        remaining variables from **subj** will also be added to the
        returned dictionary.

        :param dict subj:
            a dictionary with variables, some of which may be replacement
            variables,
        :param bool include_unmapped:
            also include the variables from **subj** which are not replacement
            variables.
        :return dict: replaced variables from *subj**.
        """
        def selfref(k, v): return subj.get(v, '$' + k) == '$' + k
        variables = {k: subj[v] for k, v in self.items() if not selfref(k, v)}
        if include_unmapped:
            mapped = set(self.values()) | set(variables)
            variables.update({k: subj[k] for k in subj if k not in mapped})
        return variables

    def _do_inject(self, dest, setter, variables):
        setter, setter_name = _method_and_name(dest, setter)
        if _is_scons_env(dest) and setter_name in _scons_env_setters:
            setter(**variables)
        else:
            for k, v in variables.items():
                setter(k, v)


class ReplacingCaller(object):
    """Base class for :class:`.ReplacingBuilder`, :class:`.ReplacingAction`
    and other similar wrappers.

    """
    def __init__(self, wrapped, replacements=dict(), **kw):
        """
        :param wrapped: callable object, initializes :attr:`.wrapped`,
        :param dict replacements: initializes :attr:`.replacements`,
        :param kw: keyword arguments used to initialize :attr:`.replacements`.
        """
        #: Wrapped callable that will be invoked with replaced variables.
        self.wrapped = wrapped
        #: An instance of :class:`.Replacements` used to replace variables.
        self.replacements = Replacements(replacements, **kw)

    def _wrapper_attributes(self):
        return ('wrapped',
                'replacements',
                'apply_replacements',
                'inject_replacements',
                '_call',
                'sort_call_args')

    def __getattr__(self, name):
        """Provides read acces to attributes of :attr:`.wrapped`."""
        return getattr(self.wrapped, name)

    def __setattr__(self, name, value):
        """Provides write access to attribtes of :attr:`.wrapped`."""
        if name in ('_wrapper_attributes',):
            raise AttributeError("can't set attribute")
        elif name in self._wrapper_attributes():
            super(ReplacingCaller, self).__setattr__(name, value)
        else:
            setattr(self.wrapped, name, value)

    def __call__(self, env, *args, **kw):
        """Invokes :attr:`.wrapped` with **args** and replaced variables in
        **env** and **kw**.

        :param env: SCons environment, an ``env.Override(...)`` will be passed
                    to :attr:`.wrapped` instead of ``env``,
        :param args: arguments to be passed to :attr:`.wrapped`,
        :param kw: keyword args (may be used to override variables in env).
        """
        return self._call(env, *args, **kw)

    def _call(self, env, *args, **kw):
        (env, kw) = self.apply_replacements(env, **kw)
        return self.wrapped(*self.sort_call_args(env, *args), **kw)

    def apply_replacements(self, env, **kw):
        """Applies replacements to env and kw."""
        ovr = self.replacements.apply(env)
        kw = self.replacements.apply(kw, True)
        return (env.Override(ovr), kw)

    def inject_replacements(self, env, setter='__setitem__',
                            only_present=False):
        """Same as :meth:`replacements.inject(self,env,setter,only_present)
        <.Replacements.inject>`."""
        self.replacements.inject(self, env, setter, only_present)

    def sort_call_args(self, *args):
        """May be be overwritten in a subclass to reorganize positional
        arguments passed to :attr:`.wrapped`."""
        return args


class ReplacingBuilder(ReplacingCaller):
    """SCons builder wrapper, calls the wrapped builder with replaced
    construction variables.

    :Example: Typical usage

    The following builder named ``MyObject`` is similar to SCons ``Object``
    builder, but it uses ``MY_CFLAGS`` instead of ``CFLAGS``.

    .. code-block:: python

        from sconstool.util import ReplacingBuilder
        from SCons.Environment import Environment

        env = Environment(tools=['default'], MY_CFLAGS=['-Wall', '-Wextra'])
        bld = ReplacingBuilder(env['BUILDERS']['Object'], CFLAGS='MY_CFLAGS')
        env['BUILDERS']['MyObject'] = bld
        bld.inject_replacements(env, 'SetDefault')

        env.MyObject('test1.c') # gcc -c -o test1.o -Wall -Wextra test1.c
        env.Object('test2.c')   # gcc -c -o test2.o test2.c
    """
    def __call__(self, env, target, source, *args, **kw):
        """Calls the wrapped builder with replaced construction variables."""
        return ReplacingCaller._call(self, env, target, source, *args, **kw)


class ReplacingAction(ReplacingCaller):
    """SCons action wrapper, replaces construction variables and calls the
    wrapped action."""

    def sort_call_args(self, env, target, source, *args):
        return (target, source, env) + args

    def __call__(self, target, source, env, *args, **kw):
        """Calls the wrapped action with replaced construction variables."""
        return ReplacingCaller._call(self, env, target, source, *args, **kw)

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:

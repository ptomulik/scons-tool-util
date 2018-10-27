# -*- coding: utf-8 -*-
"""Provides the :class:`.SrcSuffixCapturingEmitter` class.
"""


__all__ = ('ConditionalEmitter',
           'SrcSuffixCapturingEmitter',)


class ConditionalEmitter(object):
    """A callable object, which calls user-provided **emitter** when a
    predefined condition is meet."""

    __slots__ = ('_predicate', '_emitter_if', '_emitter_else')

    def __init__(self, predicate, emitter_if=None, emitter_else=None):
        """
        :param predicate:
            a callable object (function) of type ``pred(target, source, env)``;
            the function should return a boolean value; if ``pred()`` returns
            true, the :class:`.ConditionalEmitter`` will dispatch control to
            **emitter_if**, otherwise it will call **emitter_else**,
        :param emitter_if:
            an emitter function of the form ``emitter(target, source, env)``
            which gets called when ``pred()`` returns ``True``,
        :param emitter_else:
            an emitter function of the form ``emitter(target, source, env)``
            which gets called when ``pred()`` returns ``False``,
        """
        if not callable(predicate):
            raise TypeError("predicate must be callable")
        self._predicate = predicate
        self._emitter_if = emitter_if
        self._emitter_else = emitter_else

    @property
    def predicate(self):
        """The value of **predicate** parameter passed in to the constructor
        at object creation"""
        return self._predicate

    @property
    def emitter_if(self):
        """The value of **emitter_if** parameter passed in to the constructor
        at object creation, or :attr:`.default_emitter` if **emitter_if** was
        omitted."""
        return self._emitter_if or self.default_emitter

    @property
    def emitter_else(self):
        """The value of **emitter_else** parameter passed in to the constructor
        at object creation, or :attr:`.default_emitter` if **emitter_else** was
        omitted."""
        return self._emitter_else or self.default_emitter

    def default_emitter(self, target, source, env):
        """Default emitter, just returns the tuple ``(target, source)``."""
        return (target, source)

    def __call__(self, target, source, env):
        cond = self.predicate(target, source, env)
        emitter = self.emitter_if if cond else self.emitter_else
        return emitter(target, source, env)


class SrcSuffixCapturingEmitter(ConditionalEmitter):
    """A :class:`.ConditionalEmitter` enabled for source nodes whose names end
    with predefined suffix."""

    __slots__ = ('_src_suffix',)

    def __init__(self, src_suffix, emitter, fallback=None):
        """
        :param str src_suffix:
            a source suffix to be matched, if source node name ends with this
            suffix, then **emitter** is being called, otherwise **falback**
            will be called; construction variables occurring in **src_suffix**
            string will be substituted before matching,
        :param emitter:
            a callable object ``emitter(target, source, env)`` to be called
            when ``str(source[0]).endswith(src_suffix)`` is ``True``,
        :param fallback:
            a callable object ``fallback(target, source, env)`` to be called
            when ``str(source[0]).endswith(src_suffix)`` is ``False``.
        """
        self._src_suffix = src_suffix
        predicate = self.match_src_suffix
        ConditionalEmitter.__init__(self, predicate, emitter, fallback)

    @property
    def src_suffix(self):
        """The value of parameter **src_suffix** passed in to the constructor
        at object creation."""
        return self._src_suffix

    def match_src_suffix(self, target, source, env):
        """A predicate function; matches **source[0]** suffix against
        :attr:`.src_suffix`."""
        src = str(source[0])
        src_suffix = env.subst(self.src_suffix)
        return src.endswith(src_suffix)


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:

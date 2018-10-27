SrcSuffixCapturingEmitter
=========================

Description
-----------

:class:`.SrcSuffixCapturingEmitter` is a :class:`.ConditionalEmitter` with
the predefined predicate which matches source file name against user-provided
suffix.

In short, the following object

.. code-block:: python

   em = SrcSuffixCapturingEmitter('.my.suffix', emitter, fallback)

when used as

.. code-block:: python

   res = em(target, source, env)

will return the result of ``emitter(target, source, env)`` if ``source[0]``
ends with ``.my.suffix``, or will return the result of
``fallback(target, source, env)`` otherwise. Construction variables are allowed
in the suffix definition, for example

.. code-block:: python

   env['MYSUFFIX'] = '.my.suffix'
   em = SrcSuffixCapturingEmitter('$MYSUFFIX', emitter, fallback)
   # ...


.. _SCons emitter: https://scons.org/doc/production/HTML/scons-user/ch18s06.html
.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->

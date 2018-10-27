ConditionalEmitter
==================

Description
-----------

:class:`.ConditionalEmitter` is a callable object which dispatches control
between two user-provided functions: ``emitter_if`` and ``emitter_else``, both
having the following prototype:

.. code-block:: python

   emitter(target, source, env)

The :class:`.ConditionalEmitter` object is designed to be used as a `SCons
emitter`_. The decision, which of the user-provided functions shall be called,
is made based on a user-defined condition, which, again, is provided by user in
the form of a ``predicate`` function

.. code-block:: python

   predicate(target, source, env)


The ``predicate`` shall return a boolean value.

In short, the following conditional emitter

.. code-block:: python

   em = ConditionalEmitter(predicate, emitter_if, emitter_else)

when used as

.. code-block:: python

   res = em(target, source, env)

will return the result of ``emitter_if(target, source, env)`` if
``predicate(target, source, env)`` is ``True``, or will return the result of
``emitter_else(target, source, env)`` otherwise.

.. _SCons emitter: https://scons.org/doc/production/HTML/scons-user/ch18s06.html
.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->

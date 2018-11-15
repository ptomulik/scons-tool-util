ReplacingBuilder
================

Description
-----------

:class:`.ReplacingBuilder` is a wrapper for SCons builders, used to call the
wrapped builders with certain construction variables replaced. A mapping of
original variable names into their overrides is provided as a constructor
argument.


.. code-block:: python

   builder = ReplacingBuilder(env['BUILDERS']['Object'], CFLAGS='MY_CFLAGS')
   env['BUILDERS']['MyObject'] = builder

In the above example, a builder named ``MyObject`` is created which passes the
value of ``MY_CFLAGS`` instead of ``FLAGS`` to the ``Object`` builder. When
used as follows with ``gcc``

.. code-block:: python

   env.Replace(MY_CFLAGS=['-Wall', '-Wextra'])
   env.MyObject('test.c')

it will invoke compiler with ``-Wall`` and ``-Wextra`` flags

.. code-block:: console

   gcc -c -o test.o -Wall -Wextra test.c

Replacements are applied also to variables passed via builder's keyword
arguments

.. code-block:: python

   env.MyObject('test.c', MY_CFLAGS=['-Wall', '-Wextra'])

The :class:`.ReplacingBuilder` wrapper exposes
:meth:`inject_replacements()<.ReplacingCaller.inject_replacements>` method which may be used to
set the replacement variables in environment to their default values.

.. code-block:: python

   builder = ReplacingBuilder(env['BUILDERS']['Object'], CFLAGS='MY_CFLAGS')
   env['BUILDERS']['MyObject'] = builder
   builder.inject_replacements(env)
   assert env['MY_CFLAGS'] == '$CFLAGS'

Examples
--------

Shared library builder for SWIG_ generated python modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example is a simplified extract from `scons-tool-swigpy`_ tool.
The presented code implements a shared library builder named ``SwigPyShlib``
which generates shared library (or dll) with prefix ``'_'`` (SWIG convention
for generated Python modules) and suffix ``'.pyd'`` (Windows convention for
Python extension modules). The suffixes for ``SwigPyShlib``, as well as few
other values will be provided via ``SWIGPY_*`` variables. Instead of using
SWIG_ to generate ``hello_wrap.c`` file, we write such a file by hand. Instead
of loading ``_hello.pyd`` as a python module, we'll write simple ``test.c``
program that will load ``_hello.pyd`` at runtime.

:Example: Tool implementation

.. literalinclude:: replacingbuilder/swigpy/site_scons/site_tools/swigpy.py
   :language: python
   :caption: Tool module: ``site_scons/site_tools/swigpy.py``

:Example: A project using the ``swigpy`` tool

.. literalinclude:: replacingbuilder/swigpy/SConstruct
   :language: python
   :caption: Project file: ``SConstruct``

.. literalinclude:: replacingbuilder/swigpy/hello.c
   :language: c
   :caption: C file: ``hello.c``

.. literalinclude:: replacingbuilder/swigpy/hello.h
   :language: c
   :caption: Header file: ``hello.h``

.. literalinclude:: replacingbuilder/swigpy/hello_wrap.c
   :language: c
   :caption: Wrapper C file: ``hello_wrap.c``

.. literalinclude:: replacingbuilder/swigpy/hello_wrap.h
   :language: c
   :caption: Header file: ``hello_wrap.h``

.. literalinclude:: replacingbuilder/swigpy/test.c
   :language: c
   :caption: Test program: ``test.c``

.. code-block:: console
   :caption: Testing on Linux

   $ scons
   $ LD_LIBRARY_PATH='.' ./test
   Hello!!


.. _SWIG: https://swig.org/
.. _scons-tool-swigpy: https://github.com/ptomulik/scons-tool-swigpy

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->

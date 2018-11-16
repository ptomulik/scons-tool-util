ReplacingBuilder
================

Description
-----------

:class:`.ReplacingBuilder` is a wrapper for SCons builders, used to call the
wrapped builders with certain construction variables replaced. A mapping of
original variable names into their replacements is provided via constructor
arguments.


.. code-block:: python

   obj = ReplacingBuilder(env['BUILDERS']['Object'], CFLAGS='MY_CFLAGS')
   env['BUILDERS']['MyObject'] = obj

In the above example, a builder named ``MyObject`` is created which passes the
value of ``MY_CFLAGS`` instead of ``CFLAGS`` to the ``Object`` builder. When
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

   obj = ReplacingBuilder(env['BUILDERS']['Object'], CFLAGS='MY_CFLAGS')
   env['BUILDERS']['MyObject'] = obj
   obj.inject_replacements(env)
   assert env['MY_CFLAGS'] == '$CFLAGS'

Note, that replacements also alter source and target prefixes/suffixes. Let's
redefine ``MyObject`` builder as follows

.. code-block:: python

   obj = ReplacingBuilder(env['BUILDERS']['Object'], OBJSUFFIX='MY_OBJSUFFIX')
   env['BUILDERS']['MyObject'] = obj
   env['MY_OBJSUFFIX'] = '.my$OBJSUFFIX'

this builder will produce files with suffix ``'.my.o'`` if the original
``$OBJSUFFIX`` is ``'.o'``. Note, that when you wrap your own builders,
they should use original variables, like ``$OBJSUFFIX`` for suffixes, not
their replacements.

.. code-block:: python

   obj = SCons.Builder.Builder(action=SCons.Defaults.CXXAction,
                               emitter={},
                               prefix='$OBJPREFIX',   # <- not $MY_OBJPREFIX
                               suffix='$OBJSUFFIX',   # <- not $MY_OBJSUFFIX
                               src_builder=['MyCXXFile'],
                               src_suffix='$MY_CXXSUFFIX',
                               source_scanner=SCons.Tool.SourceFileScanner,
                               single_source=1)
   obj = ReplacingBuilder(obj, OBJPREFIX='MY_OBJPREFIX',
                               OBJSUFFIX='MY_OBJSUFFIX')
   env['BUILDERS']['MyObject'] = obj
   # ...
   env.SetDefault(MY_OBJSUFFIX='.my$OBJSUFFIX')


If we used ``suffix='$MY_OBJSUFFIX'`` in the above example, variable
substitution would be performed twice, and the actual suffix woule be
``'.my.my.o'`` instead of ``'.my.o'``.


Examples
--------

Shared library builder for `SWIG`_-generated python modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example is a modified extract from `scons-tool-swigpy`_ tool.
The presented code implements a shared library builder named ``SwigPyShlib``
which generates shared library (or dll) with prefix ``'_'`` (SWIG convention
for generated Python modules) and suffix ``'.pyd'`` (Windows convention for
Python extension modules). The infixes for ``SwigPyShlib``, as well as few
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

.. literalinclude:: replacingbuilder/swigpy/test_hello.c
   :language: c
   :caption: Test program: ``test_hello.c``

.. code-block:: console
   :caption: Testing on Linux

   $ scons
   $ LD_LIBRARY_PATH='.' ./test_hello
   wrap
     hello
   unwrap


.. _SWIG: https://swig.org/
.. _scons-tool-swigpy: https://github.com/ptomulik/scons-tool-swigpy

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->

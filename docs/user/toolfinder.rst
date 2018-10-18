ToolFinder
==========

.. currentmodule:: sconstool.util

:class:`.ToolFinder` is a configurable functor class used to search for files
within predefined search paths. Once created (configured), an instance of
:class:`.ToolFinder` is expected to return same search result, every time it's
applied to a given (unmodified) SCons environment.

.. code-block:: python

   python = ToolFinder('python')
   def generate(env):
      env['PYTHON'] = python(env)   # same result here ...
   def exists(env):
      return python(env)            # ... and here

The file/program being searched for is identified by a name. By default,
**tool** name is used (``'python'`` in the above example). This may be
overwritten with the ``name`` parameter

.. code-block:: python

   python = ToolFinder('python', name='python3')

The above finder will search for ``'python3'`` file for the purpose of SCons
tool named ``'python'``. Cumbersome strings may be used for ``name``,
including variable substitutions, like ``name="$PYTHONNAME"``.


By default, :class:`.ToolFinder` searches within the standard SCons PATH
(``env['ENV']['PATH']``). This can be changed, by providing ``path`` argument
to the constructor

.. code-block:: python

   # Will search in custom path, instead of env['ENV']['PATH']
   python = ToolFinder('python', path=['/home/user/.local/virtualenvs/foo/bin',
                                       '/home/user/.local/bin'])
   prog = python(env)

If file is found in ``path`` (or SCons PATH, if ``path`` not given), its name
is returned. By setting ``strip_path`` to ``False``, the object is being told
to return absolute path instead

.. code-block:: python

   # Will return absolute path to the file found
   python = ToolFinder('python', strip_path=False)
   prog = python(env)    # '/usr/bin/python', for example

:class:`.ToolFinder` accepts two extra search paths: ``priority_path``,
and ``fallback_path``. The ``priority_path`` is searched prior to the SCons
PATH, the ``fallback_path`` is examined after the SCons PATH.

.. code-block:: python

   # Will search in priority_path, then env['ENV']['PATH'], then fallback_path.
   python = ToolFinder('python', priority_path=['/home/user/.local/bin'],
                                 fallback_path=['/opt/bin'])
   prog = python(env)

It's assumed, that the priority-/fallback- paths are not known to SCons during
the build phase (later). Thus, if :class:`.ToolFinder` finds the program in
either ``priority_path`` or ``fallback_path``, it returns an absolute path.
This may be changed with ``strip_priority_path`` and ``strip_fallback_path``,
respectively

.. code-block:: python

   # if /home/user/.local/bin/python exists, python(env) will return 'python'.
   python = ToolFinder('python', priority_path=['/home/user/.local/bin'],
                                 strip_priority_path=True)

:class:`.ToolFinder` is able to automatically bind parameters ``name``,
``priority_path``, and ``fallback_path`` to prescribed construction
variables, instead of assigning them fixed values. Parameters, that enable this
feature, are: ``use_vars``, ``use_name_var``, ``use_priority_path_var``,
``use_fallback_path_var``.

.. code-block:: python

   python = ToolFinder('python', use_vars=True)
   python.name             # -> '$PYTHONNAME'
   python.priority_path    # -> '$PYTHONPATH'
   python.fallback_path    # -> '$PYTHONFALLBACKPATH'

The variable names are generated from :attr:`templates<.ToolFinder.templates>`.
They can be customized as well. For example, we can pickup another variable for
the ``priority_path`` above, instead of the unfortunate ``$PYTHONPATH`` (which
is already reserved for different purposes)

.. code-block:: python

   python = ToolFinder('python', use_vars=True,
                       templates={'fallback_path': '%(tool)sBINPATH'})
   python.fallback_path    # -> '$PYTHONBINPATH'


Iconv tool -- basic
-------------------

The :manpage:`iconv(1)` translates texts between encodings. The following
simple tool makes use of :manpage:`iconv(1)` installed in standard
location (within SCons search PATH).

:Example: ``iconv`` tool implementation, ``iconv.py`` file

.. code-block:: python

   # site_scons/site_tools/iconv.py
   from sconstool.util import *
   from SCons.Builder import Builder

   # With the following, _iconv(env) is equivalent to env.Detect('iconv')
   _iconv = ToolFinder('iconv')

   def generate(env):
      env.SetDefault(ICONV=_iconv(env))
      env.SetDefault(ICONVFROM='utf8', ICONVTO='utf8')
      env['ICONVCOM'] = '$ICONV -f $ICONVFROM -t $ICONVTO -o $TARGET $SOURCE'
      env['BUILDERS']['Iconv'] = Builder(action='$ICONVCOM')

   def exists(env):
      return _iconv(env)

:Example: sample project -- ``SConstruct`` file

.. code-block:: python

   # SConstruct
   env = Environment(tools=['iconv'])
   env.Iconv('utf8.txt', 'latin2.txt', ICONVFROM='latin2')

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->

ToolFinder
==========

Description
-----------

:class:`.ToolFinder` is a configurable functor used to search for executable
files within predefined search paths. Once created (configured), an instance of
:class:`.ToolFinder` is expected to return same search result, every time it's
applied to a given SCons environment.

.. code-block:: python

   python = ToolFinder('python')
   def generate(env):
      env['PYTHON'] = python(env)   # same result here ...
   def exists(env):
      return python(env)            # ... and here

The program being searched for is identified by a name. By default, **tool**
name is used (``'python'`` in the above example). This may be overwritten with
the ``name`` parameter

.. code-block:: python

   python = ToolFinder('python', name='python3')

The above finder will search for ``'python3'`` file for the purpose of SCons
tool named ``'python'``. Cumbersome strings may be used for ``name``,
including variable substitutions, like ``name="$PYTHONNAME"``.

.. code-block:: python

   python = ToolFinder('python', name='$PYTHONNAME')


By default, :class:`.ToolFinder` searches within the standard SCons PATH
(``env['ENV']['PATH']``). This can be changed, by providing ``path`` argument
to the constructor

.. code-block:: python

   # Will search in custom path, instead of env['ENV']['PATH']
   python = ToolFinder('python', path=['/home/user/.local/virtualenvs/foo/bin',
                                       '/home/user/.local/bin'])
   prog = python(env)

If file is found in ``path`` (or SCons PATH, if ``path`` not given), its
**name** is returned. By setting ``strip_path`` to ``False``, the object is
being told to return absolute path instead

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

The priority-/fallback- paths are used by :class:`.ToolFinder` at the tool
configuration time, but it's assumed that they're not used by SCons during the
build phase (later), when the program has to be invoked. Following this
assumption, to ensure that same program will be picked up at the build stage,
:class:`.ToolFinder` returns an absolute path to any program found within
either ``priority_path`` or ``fallback_path``. This behavior may be changed
with ``strip_priority_path`` and ``strip_fallback_path``, respectively

.. code-block:: python

   # Will return 'python', instead of '/home/user/.local/bin/python'
   python = ToolFinder('python', priority_path=['/home/user/.local/bin'],
                                 strip_priority_path=True)
   python(env)

:class:`.ToolFinder` is able to automatically bind parameters ``name``,
``priority_path``, and ``fallback_path`` to prescribed construction
variables, instead of assigning them fixed values. This feature may be enabled
with ``use_vars``, ``use_name_var``, ``use_priority_path_var``,
``use_fallback_path_var``.

.. code-block:: python

   python = ToolFinder('python', use_vars=True)
   python.name             # -> '$PYTHONNAME'
   python.priority_path    # -> '$PYTHONPRIORITYPATH'
   python.fallback_path    # -> '$PYTHONFALLBACKPATH'

The variable names are generated from :attr:`templates<.ToolFinder.templates>`,
which can be customized as well. For example, we can pickup another variable
for the ``priority_path``

.. code-block:: python

   python = ToolFinder('python', use_vars=True,
                       templates={'priority_path': '$%(TOOL)sBINPATH'})
   python.priority_path    # -> '$PYTHONBINPATH'

Examples
--------

Iconv tool
^^^^^^^^^^

The :manpage:`iconv(1)` command translates texts between encodings. The
following simple tool makes use of :manpage:`iconv(1)` installed in standard
location (within SCons search PATH).

:Example: Tool implementation

.. literalinclude:: toolfinder/iconv/site_scons/site_tools/iconv.py
   :language: python
   :caption: Tool module: ``site_scons/site_tools/iconv.py``

:Example: A project using the ``iconv`` tool

.. literalinclude:: toolfinder/iconv/SConstruct
   :language: python
   :caption: Project file: ``SConstruct``

.. literalinclude:: toolfinder/iconv/latin2.txt
   :encoding: latin2
   :caption: Input file: ``latin2.txt``

Hammer tool
^^^^^^^^^^^

This tool will use our own python script ``hammer.py`` stored in a non-standard
path. The ``hammer.py`` will replace all the occurrences of ``"nail"`` with
``"drived in nail"``.

:Example: The ``hammer`` command

.. literalinclude:: toolfinder/hammer/bin/hammer.py
   :language: python
   :caption: Command implmementation: ``bin/hammer.py``

:Example: Tool implementation

.. literalinclude:: toolfinder/hammer/site_scons/site_tools/hammer.py
   :language: python
   :caption: The tool module: ``site_scons/site_tool/hammer.py``

:Example: A project using the ``hammer`` tool.

.. literalinclude:: toolfinder/hammer/SConstruct
   :language: python
   :caption: Project file: ``SConstruct``

.. literalinclude:: toolfinder/hammer/input.txt
   :language: python
   :caption: Input file: ``input.txt``

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->

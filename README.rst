scons-tool-util
==================

.. image:: https://badge.fury.io/py/scons-tool-util.svg
    :target: https://badge.fury.io/py/scons-tool-util
    :alt: PyPi package version
.. image:: https://readthedocs.org/projects/scons-tool-util/badge/?version=latest
    :target: https://scons-tool-util.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://travis-ci.org/ptomulik/scons-tool-util.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-util
.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-util?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-util
.. image:: https://coveralls.io/repos/github/ptomulik/scons-tool-util/badge.svg?branch=master
    :target: https://coveralls.io/github/ptomulik/scons-tool-util?branch=master
.. image:: https://api.codeclimate.com/v1/badges/4c43a53855f688da6bde/maintainability
   :target: https://codeclimate.com/github/ptomulik/scons-tool-util/maintainability
   :alt: Maintainability

A little python package that helps loading externally managed SCons_ tools.

Installation
------------

To install module from pypi_, type

.. code-block:: shell

      pip install scons-tool-util

or, if your project uses pipenv_:

.. code-block:: shell

      pipenv install --dev scons-tool-util

Alternativelly, you may add this to your ``Pipfile``

.. code-block:: ini

    [dev-packages]
    scons-tool-util = "*"

This will install a namespaced package ``sconstool.util`` in project's
virtual environment.


Usage examples
--------------

TBD

More documentation
------------------

See the `online documentation`_.

LICENSE
-------

Copyright (c) 2018 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

.. _scons-tool-util: https://github.com/ptomulik/scons-tool-util
.. _SCons: http://scons.org
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/
.. _online documentation: https://scons-tool-util.readthedocs.io/

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->

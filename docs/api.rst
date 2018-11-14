API Documentation
*****************

This is an official API documentation for the scons-tool-util_ python package.

.. _Introduction:

Introduction
============

For specific documentation, please skip to the next sections.

The :mod:`sconstool.util` is an implicit namespaced package (see `PEP 420`_)
within ``sconstool`` namespace. Because of this, there is no
``lib/sconstool/__init__.py``.

.. _Classes:

Classes
=======

This section documents classes provided by scons-tool-util_ package. The
summary below provides links to a full documentation for each class.

.. currentmodule:: sconstool.util

.. autosummary::
    :toctree: api/classes
    :template: autosummary/class.rst

    ToolFinder
    ConditionalEmitter
    Selector
    Replacements
    ReplacingCaller
    ReplacingBuilder
    ReplacingAction

.. _Functions:

Functions
=========

This section documents functions provided by scons-tool-util_ package. The
summary below provides links to a full documentation for each function.

.. autosummary::
    :toctree: api/functions
    :template: autosummary/function.rst

    add_ro_dict_property
    ensure_kwarg_in
    ensure_kwarg_not_in
    check_kwarg
    check_kwargs
    import_all_from

.. _scons-tool-util: https://github.com/ptomulik/scons-tool-util
.. _PEP 420: https://www.python.org/dev/peps/pep-0420/

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->

# -*- coding: utf-8 -*-
"""scons-tool-util
"""

from setuptools import setup
from os import path
from sys import version_info


here = path.abspath(path.dirname(__file__))

if version_info < (3, 0):
    from io import open as uopen
else:
    uopen = open

readme_rst = path.join(here, 'README.rst')
with uopen(readme_rst, encoding='utf-8') as f:
    readme = f.read()

about = {}
about_py = path.join(here, 'lib', 'sconstool', 'util', 'about.py')
with open(about_py) as f:
    exec(f.read(), about)

setup(
        name='scons-tool-util',
        version=about['__version__'],
        package_dir={'': 'lib'},
        packages=['sconstool.util'],
        namespace_packages=['sconstool'],
        description='A library of utility functions and objects for ' +
                    'scons-tool-* packages',
        long_description=readme,
        long_description_content_type='text/x-rst',
        url='https://github.com/ptomulik/scons-tool-util',
        author='Paweł Tomulik',
        author_email='ptomulik@meil.pw.edu.pl'
)

# vim: set expandtab tabstop=4 shiftwidth=4:

# -*- coding: utf-8 -*-
"""scons-tool-util
"""

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

about = {}
with open(path.join(here, 'lib', 'sconstool', 'util', 'about.py')) as f:
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

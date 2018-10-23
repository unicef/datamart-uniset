#!/usr/bin/env python
import ast
import os
import re

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'uniset', '__init__.py')

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    version = str(ast.literal_eval(_version_re.search(content).group(1)))
    name = str(ast.literal_eval(_name_re.search(content).group(1)))

setup(
    name=name,
    version=version,
    description='UNICEF superset',
    long_description='',
    author='UNICEF',
    author_email='',
    url='https://github.com/unicef/uniset/',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    py_modules=['superset_config'],
    entry_points={
        'console_scripts': [
            'uniset = uniset.bin.cli:main',
        ],
    },
    include_package_data=True,
)

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, re, ast
from setuptools import setup, find_packages


PACKAGE_NAME = 'zfitter'
with open(os.path.join(PACKAGE_NAME, '__init__.py')) as f:
    match = re.search(r'__version__\s+=\s+(.*)', f.read())
version = str(ast.literal_eval(match.group(1)))
with open('requirements.txt') as f:
    requires = [
        r.split('/')[-1] if r.startswith('git+') else r
        for r in f.read().splitlines()]

setup(
    name="zfitter",
    version=version,
    url='https://github.com/mzks/zfitter',
    author='Keita Mizukoshi',
    author_email='mzks@stu.kobe-u.ac.jp',
    maintainer='Keita Mizukoshi',
    maintainer_email='mzks@stu.kobe-u.ac.jp',
    description=' zfit wrapper for lazy analysts',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requires,
    license="MIT",
    include_package_data=True,
    python_requires=">=3.7",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)

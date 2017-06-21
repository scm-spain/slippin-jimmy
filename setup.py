#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: SCMSpain
"""
from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='slippinj',
    version='1.6.0',
    author='Data Architects SCM Spain',
    author_email='data.architecture@scmspain.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    url='https://github.com/scm-spain/slippin-jimmy',
    description='Tools to generate and deploy Apache Oozie workflows',
    long_description=long_description,
    license='GPLv2',
    install_requires=open('requirements.txt').read().split(),
    scripts=['scripts/jimmy'],
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Environment :: Console'
    ],
    keywords='oozie workflows code generation emr aws'
)

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: SCMSpain
"""

from setuptools import setup, find_packages

setup(
    name='slippinj',
    version='1.1.0',
    author='Data Architects SCM Spain',
    author_email='data.architects@scmspain.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    url='https://github.schibsted.io/scmspain/data-bi-slippin-jimmy',
    description='Tools to generate and deploy Apache Oozie workflows',
    install_requires=open('requirements.txt').read().split(),
    scripts=['scripts/jimmy']
)
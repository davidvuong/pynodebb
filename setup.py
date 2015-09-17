#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pynodebb import __version__


from setuptools import setup, find_packages

setup(
    name='pynodebb',
    version=__version__,
    description='A Python client over the NodeBB REST API',
    url='https://github.com/davidvuong/pynodebb',

    author='David Vuong',
    author_email='david.vuong256@gmail.com',

    classifiers=[
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',

        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords=['nodebb', 'forums', 'api', 'client'],

    license='MIT',

    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=[
        'requests==2.7.0',
    ],
    include_package_data=True,
    package_data={'': ['README.md', 'LICENSE']},
)

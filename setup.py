#!/usr/bin/env python3

# setuptools
from setuptools import setup

# lendingclub2
from lendingclub2 import __version__

setup(
    name="lendingclub2",
    version=__version__,
    description='Help automating LendingClub processes',
    packages=['lendingclub2'],
    install_requires=[
        'requests>=2.18',
    ],
    author='Alex Hartoto',
    author_email='ahartoto.dev@gmail.com',
    url='https://github.com/ahartoto/lendingclub2',
    keywords='lendingclub python api',
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)

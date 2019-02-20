#!/usr/bin/env python3

# setuptools
from setuptools import setup

# lendingclub2
from lendingclub2 import __version__

with open('README.rst') as fin:
    long_description = fin.read()

setup(
    name="lendingclub2",
    version=__version__,
    description='Help automating LendingClub processes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['lendingclub2'],
    install_requires=[
        'requests>=2.18',
    ],
    author='Alex Hartoto',
    author_email='ahartoto.dev@gmail.com',
    url='https://github.com/ahartoto/lendingclub2',
    keywords=['lendingclub', 'lending-club', 'p2p', 'loan', 'api'],
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Office/Business :: Financial',
    ],
)

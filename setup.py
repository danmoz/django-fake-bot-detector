#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from fakebotdetector import __version__


def get_long_description():
    """Return the README"""
    return open('README.md', 'r', encoding='utf8').read()


setup(
    name='django-fake-bot-detector',
    version=__version__,
    url='https://github.com/danmoz/django-fake-bot-detector',
    license='Apache Software License',
    description='Detect and block fake search bots 🤖',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Dan Morrison',
    author_email='dan@offworld.net.au',
    packages=['fakebotdetector'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)

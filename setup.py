#!/usr/bin/env python

from setuptools import setup

setup(name='xpect',
      version='1.1.0',
      description='Programmed dialogue with interactive streams.',
      long_description=open('README.rst', 'r').read(),
      author='Erik Moqvist',
      author_email='erik.moqvist@gmail.com',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords=['expect'],
      url='https://github.com/eerimoq/expect',
      py_modules=['expect'],
      test_suite="tests")

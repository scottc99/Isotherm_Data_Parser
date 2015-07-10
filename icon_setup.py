#!/usr/bin/env python

from setuptools import setup
from distutils.core import setup
import py2exe
import os

setup(
	console = ['run.py'],
	windows = ['GUI.py']
)
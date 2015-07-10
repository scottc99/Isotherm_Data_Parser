#!/usr/bin/env python

from distutils.core import setup
import py2exe
import os

setup(
	console = ['run.py'],
	windows = ['GUI.py']
)
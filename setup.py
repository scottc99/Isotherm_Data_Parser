#!/usr/bin/env python

try:
	from distutils.core import setup
except: 
	from setuptools import setup
import py2exe, os, sys

sys.argv.append('py2exe')

setup(
    name = "Isotherm_Data_Parser",
    version = "0.1.0.dev1",
    packages = ['iso_main', 'iso_main.AMC_Files', 
                'iso_main.IGA_Files', 'iso_main.TGA_Files'],
    package_data = {'AMC_Files/Data_Files': ['Excel/*.xlsx'], 'AMC_Files/Data_Files': ['JSON/*.json'], 
                    'AMC_Files/Data_Files': ['XML/*.xml'], 'AMC_Files': ['AMC_plots/*.png'], 
                    'IGA_Files/Data_Files': ['Excel/*.xlsx'], 'IGA_Files/Data_Files': ['JSON/*.json'], 
                    'IGA_Files/Data_Files': ['XML/*.xml'], 'IGA_Files': ['IGA_plots/*.png'],
                    'TGA_Files/Data_Files': ['Excel/*.xlsx'], 'TGA_Files/Data_Files': ['JSON/*.json'], 
                    'TGA_Files/Data_Files': ['XML/*.xml'], 'TGA_Files': ['TGA_plots/*.png']},
    url = "https://github.com/scottc99/Isotherm_Data_Parser",
    author = "NIST: Group 642, 643 Contributers",
    author_email = "scottc99@students.rowan.edu",
    description = "A tool designed to parse through isotherm data and convert data into json and xml formats and plot.",
    install_requires = ['setuptools', 'matplotlib>=1.4.3', 'numpy',
                        'simplejson>=3.7.3', 'xlrd>=0.9.3', 'xlwt>=0.7.5',
                        'dicttoxml>=1.6.6', 'lxml', 'libxml2dom', 'py2exe'],
    windows=[{"script":"iso_main/run.py"}]
)

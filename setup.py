#!/usr/bin/env python

from distutils.core import setup
import os

setup(
    name = "Isotherm_Data_Parser",
    version = "0.1.0.dev1",
    packages = ['iso_main', 'iso_main.AMC_Files', 
                'iso_main.IGA_Files', 'iso_main.TGA_Files'],
    url = "https://github.com/scottc99/Isotherm_Data_Parser",
    author = "NIST: Group 642, 643 Contributers",
    author_email = "scottc99@students.rowan.edu",
    description = "A tool designed to parse through isotherm data and convert data into json and xml formats and plot.",
    install_requires = ['setuptools >= 17.0', 'matplotlib >= 1.4.3', 'numpy >= 1.9.2', 
                        'simplejson >= 3.7.3', 'xlrd >= 0.9.3', 'xlwt >= 0.7.5', 
                        'pprint >= 0.2.3', 'codecs >= 7.8', 'collections', 
                        'dicttoxml >= 1.6.6', 'lxml >= 3.4.2', 'libxml2 >= 2.9.0', 
                        'libxslt >= 1.1.26'],
    entry_points={
        'console_scripts': [
            'Isotherm_Data_Parser = Isotherm_Data_Parser.run:main'
        ]
    }        
)


#!/usr/bin/env python

from setuptools import setup
from codecs import open 
import os

setup(
    name = "Isotherm_Data_Parser",
    version = "0.1.0.dev1",
<<<<<<< HEAD
    package_dir = {'site-packages': ''},
    packages = ['pip', 'matplotlib', 'matplotlib.pyplot', 'matplotlib.pyplot.show', 
                'matplotlib.pyplot.plot', 'matplotlib.pyplot.ion', 'numpy', 'lxml', 
                'simplejson', 'xlrd', 'xlwt'],
    py_modules = ['glob', 'time', 'pprint', 'codecs', 'collections',
                    'dicttoxml', 'pylab'],
=======
    packages = ['site-packages', 'setuptools', 'setuptools.setup', 'codecs', 'codecs.open', 'collections', 'collections.OrderedDict',
                'Tkinter', 'Tkinter.*', 'matplotlib.pyplot', 'matplotlib.pyplot.show', 'matplotlib.pyplot.plot', 
                'matplotlib.pyplot.ion', 'json', 'lxml', 'glob', 'xlrd', 'xlwt', 'simplejson', 'matplotlib', 'pylab', 
                'numpy', 'dicttoxml', 'lxml', 'time'],
>>>>>>> 5611d5f23d741c643e1454f9f48f9ae77b4050c2
    url = "https://github.com/scottc99/Isotherm_Data_Parser",
    author = "NIST: Group 642, 643 Contributers",
    author_email = "scottc99@students.rowan.edu",
    description = "A tool designed to parse through isotherm data and convert data into json and xml formats and plot. ",
    long_description = open('README.rst').read(),
    install_requires = ['libxml2 >= 2.9.0', 'libxslt >= 1.1.26'],
    entry_points={
        'console_scripts': [
            'Isotherm_Data_Parser = Isotherm_Data_Parser.run:main'
        ]
    }        
)


# setup.py
# Setup module for the Dexter project
#

from setuptools import setup

setup(name='dexter',
    version='0.1',
    description='Malware proof of concept',
    url='http://github.com/freeloader0/dexter',
    author='Freeloader0',
    author_email='',
    license='MIT',
    packages=['dexter'],
    install_requires=[
        'py2Exe',
    ],
	zip_safe=False)
  
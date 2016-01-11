# py2ExeSetup.py
# Script to make a Windows executable out of any Python script passed as input
# USAGE: python py2ExeSetup.py <PYTHON_SCRIPT_TO_CONVERT>
# 

from distutils.core import setup
import py2exe
from sys import *


def main():
    if len(argv) != 2:
        print('USAGE: python py2ExeSetup.py <PYTHON_SCRIPT_TO_CONVERT>')
        exit(-1)
    else:
        target = str(argv[1])
        argv[1] = 'py2exe'
        setup(console=[target])
    
if __name__ == '__main__':
    main()

# py2ExeSetup.py
# Script to make a Windows executable out of any Python script passed as input
#
# USAGE: python py2ExeSetup.py <PYTHON_SCRIPT_TO_CONVERT>
# Input: Python script to be converted to a .exe
# Output: Absolute path to the resulting .exe
# 

from distutils.core import setup
import py2exe
import os
from sys import *


def makeExe(target=None):
    # Ensure correct usage
    if target == None and len(argv) != 2:
        print('USAGE: python py2ExeSetup.py <PYTHON_SCRIPT_TO_CONVERT>')
        exit(-1)
    # If no target is passed in, assume it's been provided in sys.argv    
    elif target == None:
        target = str(argv[1])
    # Fix argv being too short
    elif len(argv) < 2:
        argv.append('py2exe')
    # Fix argv being too long
    else:
        while len(argv) > 2:
            argv.pop()

    argv[1] = 'py2exe'
    setup(console=[target])
    return os.path.join(os.getcwd(), 'dist', str(target[:-2] + 'exe'))
    
if __name__ == '__main__':
    makeExe()

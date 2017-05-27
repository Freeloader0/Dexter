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
import sys
from Dexter.comms import *

def makeExe(target=None):
    # Ensure correct usage
    if target == None and len(sys.argv) != 2:
        print('USAGE: python py2ExeSetup.py <PYTHON_SCRIPT_TO_CONVERT>')
        exit(-1)
    # If no target is passed in, assume it's been provided in sys.argv    
    elif target == None:
        target = str(sys.argv[1])
    # Fix argv being too short
    elif len(sys.argv) < 2:
        sys.argv.append('py2exe')
    # Fix argv being too long
    else:
        while len(sys.argv) > 2:
            sys.argv.pop()

    # Ensure critical Dexter modules are included in .exe creation
    includes = ["json"]
    for k in sys.modules.keys():
        if k[:13] == 'Dexter.comms.':
            includes.append(k)
    
    sys.argv[1] = 'py2exe'
    setup(console=[{"script":target}], options={"py2exe":{"includes":includes}})
    return os.path.join(os.getcwd(), 'dist', str(target[:-2] + 'exe'))
    
if __name__ == '__main__':
    makeExe()

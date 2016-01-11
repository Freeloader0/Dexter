# runSystemCommand.py
# Script to run a Windows system command and return the output
#

from sys import *
import subprocess

# Function expects an ordered list of the Windows command, incl. parameters
def runSystemCommand(cmd):
    return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    del(argv[0])
    print(runSystemCommand(argv))
        
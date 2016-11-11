# dexter.py
# Main module of the Dexter project
#
# This file should specify WHAT Dexter should do while other modules
# will specify HOW Dexter will do it
#

# Imports
import datetime
import os.path
import argparse
import string
import json
import importlib

# Local Dexter imports
from getHostInfo import *

# Global variables
environ = getHostInfo()


# Function to write a string into the Dexter Log
def writeLog(message, debug=False):
    message = str(datetime.datetime.now()) + ': ' + message + '\r\n'
    
    # Assert that the log file has been designated
    if 'DEXTERLOG' not in environ.keys():
        environ['DEXTERLOG'] = str(os.path.join(environ['ALLUSERSPROFILE'], 'dexter.log'))
       
    # Attempt to write to log file
    try:
        with open(environ['DEXTERLOG'], 'a') as f:
            f.write(message)
            
        if debug:
            print(message)
            
    except:
        return -1
        
    return 0

    
# Main subroutine    
def main():
    #
    # INITIAL SETUP
    #
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('server', help='address of server')
    parser.add_argument('port', type=int, help='port number of server')    
    parser.add_argument('comms', help='dexter communications module to use')
    parser.add_argument('--beaconInterval', type=int, default=60, help='interval between beacons, in seconds.  defaults to 60')
    parser.add_argument('--debug', action='store_true', default=False, help='flag to print dexter debug messages')
    args = parser.parse_args()
    debug = args.debug
    
    environ['BEACON'] = args.beaconInterval
    environ['DEXTERSERVER'] = args.server
    environ['DEXTERPORT'] = args.port
    # TODO: Add initial command as a command-line argument.  Should this be JSON?
    # ALSO: Make an HTTPS mod to test multiple comms mods
    
    commLib = importlib.import_module('comms.' + args.comms)
    commModule = commLib.commClass(args.server, args.port)
    
    writeLog('Dexter Started', debug)
    
    response = commModule.checkIn({'DEXTERID' : environ['DEXTERID'], 'ENVIRONMENT' : environ})
    print(response)
    
    #
    # Main Control Loop
    #
    
    writeLog('Dexter Stopped', debug)
    pass

if __name__ == '__main__':
    main()
        
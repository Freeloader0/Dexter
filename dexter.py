# dexter.py
# Main module of the Dexter project
#

# Imports
import datetime
import os.path


# Local Dexter imports
from getHostInfo import *


# Global variables
environ = getHostInfo()


# Function to write a string into the Dexter Log
def writeLog(message):
    message = str(datetime.datetime.now()) + ': ' + message + '\r\n'
    
    # Assert that the log file has been designated
    if 'DEXTERLOG' not in environ.keys():
        environ['DEXTERLOG'] = str(os.path.join(environ['PUBLIC'], 'dexter.log'))
       
    # Attempt to write to log file
    try:
        with open(environ['DEXTERLOG'], 'a') as f:
            f.write(message)
    except:
        return -1
        
    return 0

    
# Main subroutine    
def main():
    writeLog('Dexter Started')
    
    pass

if __name__ == '__main__':
    main()
        
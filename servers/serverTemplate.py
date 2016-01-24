# serverTemplate.py
# Server class for Dexter server-side modules.  Specifies which functions must be
# implemented by underlying submodules that will do the actual data transport
#

import datetime
import os.path

class serverTemplate():

    def __init__(self):
        pass
    
    # Function to write a string into the server log
    def writeServerLog(logfile, message):
        message = str(datetime.datetime.now()) + ': ' + message + '\r\n'
           
        # Attempt to write to log file
        try:
            with open(logfile, 'a') as f:
                f.write(message)
        except:
            return -1
            
        return 0

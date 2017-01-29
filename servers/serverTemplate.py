# serverTemplate.py
# Server class for Dexter server-side modules.  Specifies which functions must be
# implemented by underlying submodules that will do the actual data transport
#

import datetime
import os.path
import json

class serverTemplate():

    def __init__(self):
        self.server = None
        pass


# Function to write a string into the server log
def writeServerLog(message, log):
    message = str(datetime.datetime.now()) + ': ' + message + '\r\n'
       
    # Attempt to write to log file
    try:
        with open(log, 'a') as f:
            f.write(message)
    except:
        return -1
        
    return 0


# Function to parse JSON-formatted server configuration files
def readConfigFile(configFile):
    configData = None
    with open(configFile, 'rb') as f:
        configData = json.loads(str(f.read(), 'utf-8'))
    f.close()
    
    return configData

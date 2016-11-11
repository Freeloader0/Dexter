# commTemplate.py
# Communications class for Dexter modules.  Specifies which functions must be
# implemented by underlying submodules that will do the actual data transport
#

import socket
import os


class commTemplate():

    def __init__(self):
        pass
    
    def checkIn(self, dexterData):
        return 'Not implemented'

    def sendEnvironment(self, environString):
        return 'Not implemented'

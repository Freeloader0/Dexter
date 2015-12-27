# getHostInfo.py
# Script to return information about a host 
#

import os
import socket
import winreg
from uuid import getnode

def getHostInfo():
    info = os.environ
    info['CURRENTPID'] = str(os.getpid())

    # Query registry to find exact Windows version
    aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)    
    with winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
        info['OSVERSION'] = winreg.QueryValueEx(key, 'ProductName')[0]
        
    # Get networking information
    # TODO: Get all MAC and IP addresses
    info['IPADDRESS'] = socket.gethostbyname(socket.gethostname())
    info['MACADDRESS'] = str(hex(getnode()))[2:]
    if len(info['MACADDRESS']) == 11:
        info['MACADDRESS'] = '0' + info['MACADDRESS']
    return info

if __name__ == '__main__':
    data = getHostInfo()
    info = list(data.keys())
    info.sort()
    for i in info:
        print(i + ': ' + str(data[i]))
        
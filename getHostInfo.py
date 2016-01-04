# getHostInfo.py
# Script to return information about a host 
#

import os
import socket
import winreg
from runSystemCommand import *
import string

def getHostInfo():
    try:
        info = dict(os.environ)
    except:
        info = dict()
    
    try:
        info['CURRENTPID'] = str(os.getpid())
    except:
        info['CURRENTPID'] = 'unknown'

    # Query registry to find exact Windows version
    try:
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)    
        with winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
            info['OSVERSION'] = winreg.QueryValueEx(key, 'ProductName')[0]
    except:
        info['OSVERSION'] = 'unknown'
        
    # Get networking information
    info['MAINIP'] = socket.gethostbyname(socket.gethostname())
    info['IPADDRESS'] = list()
    info['MACADDRESS'] = list()
    lines = str.split(str(runSystemCommand(['ipconfig', '/all'])), '\\r\\n')
    for l in lines:
        if str.find(l, 'Physical Address') > -1:
            info['MACADDRESS'].append(str.split(l)[-1])
        elif str.find(l, 'IPv4 Address.') > -1 or str.find(l, 'IPv6 Address.') > -1 or str.find(l, 'IP Address.') > -1:
            info['IPADDRESS'].append(str.split(l)[-1].replace('(Preferred)', ''))
        
    return info

if __name__ == '__main__':
    data = getHostInfo()
    info = list(data.keys())
    info.sort()
    for i in info:
        print(i + ': ' + str(data[i]))
        
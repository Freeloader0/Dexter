# dexterTests.py
# Unit testing for project Dexter
#
# Last updated: 1/11/2016
#
# Functions supported:
### runSystemCommand
### getHostInfo
### dexter.writeLog
### makeExe
### HTTP client comms
# Functions TODO:
### HTTP server comms response
#

import unittest
import os
from subprocess import CalledProcessError
import multiprocessing
import json
import tempfile

# Dexter specific imports
from Dexter.dexter import *
from Dexter.getHostInfo import *
from Dexter.runSystemCommand import *
from Dexter.py2ExeSetup import *
from Dexter.servers import *
from Dexter.comms import *

class testRunSystemCommand(unittest.TestCase):

    def testRunSystemCommand_correct(self):
        self.assertIsInstance(runSystemCommand('ipconfig'), bytes)

    def testRunSystemCommand_badInput(self):
        self.assertRaises(CalledProcessError, runSystemCommand, ['del'])        


class testGetHostInfo(unittest.TestCase):

    def testGetHostInfo_correct(self):
        info = getHostInfo()
        self.assertIsInstance(info, dict)
        self.assertTrue('DEXTERID' in info.keys())
        
        
class testDexterWriteLog(unittest.TestCase):

    def testGetHostInfo_correct(self):
        self.assertIsInstance(environ, dict)
        self.assertEqual(writeLog('Dexter Test'), 0)
        self.assertIsInstance(environ['DEXTERLOG'], str)
        self.assertTrue(os.path.exists(environ['DEXTERLOG']))

        
class testMakeExe(unittest.TestCase):

    def testMakeExe_correct(self):
        exePath = os.path.join(os.getcwd(), 'dist', 'getHostInfo.exe')
        if os.path.exists(exePath):
            os.remove(exePath)
        newPath = makeExe('getHostInfo.py')
        self.assertEqual(exePath, newPath)
        self.assertTrue(os.path.exists(newPath))
        

# HTTP Comm module test class and helper function     
def httpTestServer(configFile):
    p = multiprocessing.current_process()
    template = dexterHttpServer.dexterHttpTemplate(configFile, verbose=False)
    httpd = template.server((template.host, template.port), dexterHttpServer.MyHandler)
    httpd.serve_forever()
    pass

    
class testHttpComms(unittest.TestCase):

    def testCheckIn_correct(self):
        # Setup
        tempLogFile = 'dexterTestLogFile.txt'
        tempConfigFile = open('dexterTestConfigFile.txt', 'wb')
        tempConfigFile.write(json.dumps({'host' : '127.0.0.1', 'port' : 12345, 'logfile' : tempLogFile}).encode('utf-8'))
        tempConfigFile.flush()
        tempConfigFile.close()
        serverProcess = multiprocessing.Process(name='HTTP Server', target=httpTestServer, args=('dexterTestConfigFile.txt',))
        serverProcess.daemon = True
        serverProcess.start()
        
        client = httpModule.commClass('127.0.0.1', 12345)
        serverResponse = client.checkIn({'DEXTERID' : 'TESTTESTTEST'})
        
        # Verify the client received a successful server response
        self.assertEqual(serverResponse, {'Status' : 'Received'})
        
        # Verify the server received a successful client message
        with open(tempLogFile, 'rb') as tempLogFileHandle:
            data = tempLogFileHandle.read().decode('utf-8')
        self.assertNotEqual(data.find('"POST /dexter.html HTTP/1.1" 200'), -1)
        self.assertNotEqual(data.find('Successful connection from 127.0.0.1: TESTTESTTEST'), -1)
        
        # Cleanup
        serverProcess.terminate()
        os.remove('dexterTestConfigFile.txt')
        os.remove(tempLogFile)
        pass
     
    def testCheckIn_noServer(self):
        # Setup     
        client = httpModule.commClass('127.0.0.1', 12345)
        serverResponse = client.checkIn({'DEXTERID' : 'TESTTESTTEST'})
        
        # Verify the client received a failure response
        self.assertEqual(serverResponse, {'Status' : 'Failed'})
        pass
    
    def testCheckIn_noDexterId(self):
        # Setup
        tempLogFile = 'dexterTestLogFile.txt'
        tempConfigFile = open('dexterTestConfigFile.txt', 'wb')
        tempConfigFile.write(json.dumps({'host' : '127.0.0.1', 'port' : 12345, 'logfile' : tempLogFile}).encode('utf-8'))
        tempConfigFile.flush()
        tempConfigFile.close()
        serverProcess = multiprocessing.Process(name='HTTP Server', target=httpTestServer, args=('dexterTestConfigFile.txt',))
        serverProcess.daemon = True
        serverProcess.start()      
        
        client = httpModule.commClass('127.0.0.1', 12345)
        serverResponse = client.checkIn({'NOTANID' : 'TESTTESTTEST'})
        
        # Verify the client received a failed to send response
        self.assertEqual(serverResponse, {'Status' : 'Failed'})
        
        # Verify the server received an improperly formatted client message
        with open(tempLogFile, 'rb') as tempLogFileHandle:
            data = tempLogFileHandle.read().decode('utf-8')
        self.assertNotEqual(data.find('"POST /dexter.html HTTP/1.1" 200'), -1)
        self.assertNotEqual(data.find('Improperly formatted connection from 127.0.0.1'), -1)
        
        # Cleanup
        serverProcess.terminate()
        os.remove('dexterTestConfigFile.txt')
        os.remove(tempLogFile)
        pass
        
        
        
if __name__ == '__main__':
    unittest.main(buffer=True)

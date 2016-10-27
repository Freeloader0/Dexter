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
def httpTestServer(logfile):
    p = multiprocessing.current_process()   
    server = dexterHttpServer.dexterHttpServer('127.0.0.1', 12345, logfile, False)
    httpd = server.server(('127.0.0.1', 12345), dexterHttpServer.MyHandler)
    httpd.serve_forever()
    pass

    
class testHttpComms(unittest.TestCase):

    def testCheckIn_correct(self):
        # Setup
        tempLogFile = 'unittest.log'
        if os.path.exists(tempLogFile):        
            os.remove(tempLogFile)
        serverProcess = multiprocessing.Process(name='HTTP Server', target=httpTestServer, args=(tempLogFile,))
        serverProcess.daemon = True
        serverProcess.start()        
        
        client = httpModule.commClass('127.0.0.1', 12345)
        serverResponse = client.checkIn(json.dumps({'DEXTERID' : 'TESTTESTTEST'}))
        
        # Verify the client received a successful server response
        self.assertEqual(serverResponse, bytes('Received', 'ascii'))
        
        # Verify the server received a successful client message
        with open(tempLogFile, 'rb') as f:
            data = f.read().decode('ascii')       
        self.assertNotEqual(data.find('"POST /dexter.html HTTP/1.1" 200'), -1)
        self.assertNotEqual(data.find('Successful connection from 127.0.0.1: TESTTESTTEST'), -1)
        
        # Cleanup
        f.close()        
        serverProcess.terminate()
        os.remove(tempLogFile)
        pass

        
        
        
if __name__ == '__main__':
    unittest.main(buffer=True)

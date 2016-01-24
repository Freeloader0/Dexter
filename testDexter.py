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
# Functions TODO:
### Server comms
### Client comms
#

import unittest
import os
from subprocess import CalledProcessError

# Dexter specific imports
from dexter import *
from getHostInfo import *
from runSystemCommand import *
from py2ExeSetup import makeExe


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

        
if __name__ == '__main__':
    unittest.main(buffer=True)

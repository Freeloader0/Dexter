# dexterTests.py
# Unit testing for project Dexter
#
# Last updated: 1/11/2016
#
# Functions supported:
### runSystemCommand
### getHostInfo
### dexter.writeLog
# Functions TODO:
### None :)

import unittest
import os.path

# Dexter specific imports
from dexter import *
from getHostInfo import *
from runSystemCommand import *
from subprocess import CalledProcessError


class testRunSystemCommand(unittest.TestCase):

    def testRunSystemCommand_correct(self):
        self.assertIsInstance(runSystemCommand('ipconfig'), bytes)

    def testRunSystemCommand_badInput(self):
        self.assertRaises(CalledProcessError, runSystemCommand, ['del'])        


class testGetHostInfo(unittest.TestCase):

    def testGetHostInfo_correct(self):
        self.assertIsInstance(getHostInfo(), dict)
        
        
class testDexterWriteLog(unittest.TestCase):

    def testGetHostInfo_correct(self):
        self.assertIsInstance(environ, dict)
        self.assertEqual(writeLog('Dexter Test'), 0)
        self.assertIsInstance(environ['DEXTERLOG'], str)
        self.assertTrue(os.path.exists(environ['DEXTERLOG']))

        
if __name__ == '__main__':
    unittest.main()

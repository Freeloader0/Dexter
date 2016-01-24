# httpModule.py
# HTTP client communications module for Dexter.
#


import urllib.request
import string
import socket
import sys
import binascii
import argparse

# Dexter specific imports
import dexter
import commTemplate


class httpComm(commTemplate.commTemplate):
    # Init function
    def __init__(self, server, port):
        self.server = server
        self.port = port
        pass

    # Function to query for tasking
    def getTasking(self):
        # Query scrape page for tasking
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/dexter.html'
        headers = {'User-Agent' : 'Dexter 1.0',
                   'Accept-Encoding' : 'gzip',
                   'Connection' : 'Close'}
        req = urllib.request.Request(url, bytes('Dexter, reporting for duty!', 'ascii'), headers)
        page = urllib.request.urlopen(req, timeout=20)
        response = page.read()
        print(response)
        return response


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('server', help='address of server')
    parser.add_argument('port', type=int, help='port number of server')
    args = parser.parse_args()
    
    mod = httpComm(args.server, args.port)
    mod.getTasking()
    

    pass	
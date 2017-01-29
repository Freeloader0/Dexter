# dexterHttpServer.py
# Server to accept HTTP comms from Dexter clients.
#

import time
import http.server
import argparse
import json
import os.path
from Dexter.servers import serverTemplate


class dexterHttpTemplate(serverTemplate.serverTemplate):
    def __init__(self, configFile, verbose=False):
        configData = serverTemplate.readConfigFile(configFile)

        # Assert that configFile contains a valid host
        try:
            self.host = configData['host']
            if type(self.host) is not str:
                raise
        except:
            print('ERROR: No valid host designator found in server config file.  A valid host is needed to run this type of server.')
            exit()
        
        # Assert that configFile contains a valid port number
        try:
            self.port = configData['port']
            if type(self.port) is not int:
                raise
        except:
            print('ERROR: No valid port number found in server config file.  A valid port number is needed to run this type of server.')
            exit()
        
        self.server = http.server.HTTPServer
        self.server.verbose = verbose
        
        # Determine if configFile contains a valid logfile path
        try:
            if 'logfile' in configData.keys() and configData['logfile'] != "None" and configData['logfile'] != None:
                self.server.logfile = configData['logfile']
            else:
                self.server.logfile = None
        except:
            print('ERROR: Invalid logfile found in server config file.')
            exit()     
        
        pass    


# Custom HTTP request handler.  Validation of Dexter comms occurs here.
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        pass
        
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-Location", "index.html")
        s.send_header("Vary", "negotiate,Accept-Encoding")
        s.send_header("TCN", "choice")
        s.send_header("Pragma", "no-cache")
        s.send_header("Connection", "close")
        s.send_header("Content-type", "text/plain")
        s.end_headers()
        s.wfile.write(bytes("Website under construction", 'ascii'))     
        pass
        
    def do_POST(s):
        if len(s.path) >= 7 and s.path[:7] == '/dexter':
            s.send_response(200)
            s.send_header("Content-Location", "dexter.html")
            s.send_header("Vary", "negotiate,Accept-Encoding")
            s.send_header("TCN", "choice")
            s.send_header("Pragma", "no-cache")
            s.send_header("Connection", "close")
            s.send_header("Content-type", "text/plain")
            s.end_headers()
            postData = json.loads(str(s.rfile.read(int(s.headers.get_all('Content-Length')[0])), 'utf-8'))
            
            # Validate if the POST was from a Dexter client
            if postData and 'DEXTERID' in postData.keys() and s.headers.get_all('User-Agent')[0] == 'Dexter 1.0':
                message = 'Successful connection from ' + s.client_address[0] + ': ' + postData['DEXTERID']
                if s.server.verbose == True:
                    print(message)
                serverTemplate.writeServerLog(message, s.server.logfile)
                s.wfile.write(bytes(json.dumps({'Status' : 'Received'}), 'ascii'))
            else:                     
                message = 'Improperly formatted connection from ' + s.client_address[0]
                if s.server.verbose == True:
                    print(message)                
                serverTemplate.writeServerLog(message, s.server.logfile)
                s.wfile.write(bytes("Website under construction", 'ascii'))
            
        else:
            s.send_response(404)
        pass
        
    def log_message(self, format, *args):
        message = str("%s - - [%s] %s" %
                (self.address_string(),
                self.log_date_time_string(),
                format%args))
        serverTemplate.writeServerLog(message, self.server.logfile)
        if self.server.verbose == True:
            print(message)
    pass


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('configFile', help='JSON-formatted file with server config info')
    parser.add_argument('-v', action='store_true', default=False, help='verbose mode. print incoming connections to the terminal')
    args = parser.parse_args()
    
    # Start server
    template = dexterHttpTemplate(args.configFile, verbose=args.v)
    httpd = template.server((template.host, template.port), MyHandler)
    print(time.asctime(), "Server Started - %s:%s" % (template.host, template.port))
    serverTemplate.writeServerLog("Server Started - %s:%s" % (template.host, template.port), template.server.logfile)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stopped - %s:%s" % (template.host, template.port))
    serverTemplate.writeServerLog("Server Stopped - %s:%s" % (template.host, template.port), template.server.logfile)
    pass


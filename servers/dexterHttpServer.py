# dexterHttpServer.py
# HTTP server to accept data from Dexter clients.
#

import time
import http.server
import argparse
from Dexter.servers import serverTemplate


class dexterHttpServer(serverTemplate.serverTemplate):
    # TODO: Figure out a better way to specify a log file without global variables
    def __init__(self, host, port, logfile, verboseParam):
        self.host = host
        self.port = port
        self.server = http.server.HTTPServer
        global serverLogFile
        serverLogFile = logfile
        global verbose
        verbose = verboseParam
        pass    


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
            postData = str(s.rfile.read(int(s.headers.get_all('Content-Length')[0])), 'utf-8')
            
            # Validate if the POST was from a Dexter client
            if s.headers.get_all('User-Agent')[0] == 'Dexter 1.0':
                message = 'Successful connection from ' + s.client_address[0] + ': ' + postData
                if verbose == True:
                    print(message)
                serverTemplate.writeServerLog(message, serverLogFile)
                s.wfile.write(bytes("Received", 'ascii'))
            else:                     
                s.wfile.write(bytes("Website under construction", 'ascii'))
            
        else:
            s.send_response(404)  
        pass
        
    def log_message(self, format, *args):
        message = str("%s - - [%s] %s" %
                (self.address_string(),
                self.log_date_time_string(),
                format%args))
        serverTemplate.writeServerLog(message, serverLogFile)
        if verbose == True:
            print(message)
    pass


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='host interface to run server on')
    parser.add_argument('port', type=int, help='port number to run server on')
    parser.add_argument('log', help='path to server log file')
    parser.add_argument('-v', action='store_true', default=False, help='verbose mode. print incoming connections to the terminal')
    args = parser.parse_args()
    
    # Start server
    template = dexterHttpServer(args.host, args.port, args.log, args.v)
    httpd = template.server((args.host, args.port), MyHandler)
    print(time.asctime(), "Server Started - %s:%s" % (args.host, args.port))
    serverTemplate.writeServerLog("Server Started - %s:%s" % (args.host, args.port), serverLogFile)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stopped - %s:%s" % (args.host, args.port))
    serverTemplate.writeServerLog("Server Stopped - %s:%s" % (args.host, args.port), serverLogFile)
    pass


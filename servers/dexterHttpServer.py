# dexterHttpServer.py
# HTTP server to accept data from Dexter clients.
#

import time
import http.server
import argparse
import serverTemplate

serverLogFile = ''

class dexterHttpServer(serverTemplate.serverTemplate):
    def __init__(self, host, port, log):
        self.host = host
        self.port = port
        self.log = log
        self.server = http.server.HTTPServer
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
                print('Client connected: ' + postData)
                s.wfile.write(bytes("Received", 'ascii'))
            else:                     
                s.wfile.write(bytes("Website under construction", 'ascii'))
            
        else:
            s.send_response(404)  
        pass


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='host interface to run server on')
    parser.add_argument('port', type=int, help='port number to run server on')
    parser.add_argument('log', help='path to server log file')
    args = parser.parse_args()
    serverLogFile = args.log
    
    # Start server
    template = dexterHttpServer(args.host, args.port, args.log)
    httpd = template.server((args.host, args.port), MyHandler)
    print(time.asctime(), "Server Started - %s:%s" % (args.host, args.port))
    template.writeServerLog("Server Started - %s:%s" % (args.host, args.port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stopped - %s:%s" % (args.host, args.port))
    template.writeServerLog("Server Stopped - %s:%s" % (args.host, args.port))
    pass


import http.server
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer

class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("hello!".encode("utf-8")))
        
        
PORT=8080


httpd = HTTPServer(("", PORT), HttpProcessor)
print('run on', PORT, 'port')
httpd.serve_forever()

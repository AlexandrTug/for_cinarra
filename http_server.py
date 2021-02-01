
import http.server
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests


class HttpProcessor(BaseHTTPRequestHandler):

    habr_url = 'https://habr.com'
    tag_open = '<'
    tag_close = '>'
    in_tag = False
    is_space = False
    is_char = False
    char_count = 0
    space_set = {' ', ',', '.', '!', ':', ';', '?', '\n', '\r'}

    def ins_TM(self, in_text):

        out_text = ''
        for i in range(len(in_text)):

            if in_text[i] == self.tag_open :
                if self.char_count == 6:
                    out_text += u"\u2122" 
                self.in_tag = True
                self.char_count = 0

            elif in_text[i] == self.tag_close : 
                self.in_tag = False

            elif (not(self.in_tag) and (in_text[i] in self.space_set)) :
                self.is_space = True
                if self.char_count == 6:
                    out_text += u"\u2122"
                self.char_count = 0

            elif not(self.in_tag):
                self.is_char = True
                self.char_count += 1
            
            out_text += in_text[i]    

        return out_text

    def do_GET(self):

        print('receive command:', self.command)
        print('path:', self.path)
        print('requestline:', self.requestline)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        r=requests.get(self.habr_url+self.path)
        localhost_text = r.text.replace(self.habr_url, 'http://localhost:'+str(PORT))
        rep_text = self.ins_TM(localhost_text)
        self.wfile.write(rep_text.encode('utf-8'))
    
 
PORT=8080


httpd = HTTPServer(("", PORT), HttpProcessor)
print('run on', PORT, 'port')
httpd.serve_forever()

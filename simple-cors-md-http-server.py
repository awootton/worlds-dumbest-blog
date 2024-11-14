#!/usr/bin/env python3

# Attribution: https://stackoverflow.com/questions/21956683/enable-access-control-on-simple-http-server

# Python 3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test as test_orig
import sys
import markdown2

def test (*args):
    test_orig(*args, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)

class CORSMDRequestHandler (SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith(".md") or self.path == "/":
            try:
                if self.path == "/":
                    self.path = "/README.md"
                with open(self.path[1:], 'r') as file:
                    markdown_text = file.read()
                html = markdown2.markdown(markdown_text)
                reply = '<html lang="en">\n<head></head>\n<body>\n'
                reply = reply + html   
                reply = reply + "\n</body></html>"
                reply = reply.encode('utf-8')
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", len(reply))
                self.end_headers()
                self.wfile.write(reply)
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            super().do_GET()
            
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)



if __name__ == '__main__':
    test(CORSMDRequestHandler, HTTPServer)
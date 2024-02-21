from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir
from os.path import join as pjoin

class Server(BaseHTTPRequestHandler):
    data_path = pjoin(curdir, 'node_data.json')

    def _make_headers(self,header, content):
        self.send_response(200)
        self.send_header(header,content)
        self.end_headers()
        
    def do_GET(self):
        if self.path == '/node_data.json':
            with open(self.data_path,'rb') as fh:
                self._make_headers('Content-type', 'application/json')
                self.wfile.write(fh.read())

    def do_POST(self):
        if self.path == '/node_data.json':
            length = self.headers['content-length']
            data = self.rfile.read(int(length))

            with open(self.data_path, 'wb') as fh:
                fh.write(data)

            self.send_response(200)
        
def run_server(server=HTTPServer, handler=Server, port=8008):
    url = ('', port)
    http_server = server(url, handler)
    
    print('Starting http-server on port %d...' % port)
    http_server.serve_forever()

if __name__ == '__main__':
    run_server()

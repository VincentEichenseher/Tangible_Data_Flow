from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir
from os.path import join as pjoin

import json

class Server(BaseHTTPRequestHandler):
    data_path = pjoin(curdir, 'node_data.json')
    edit_path = pjoin(curdir, 'stack_data.json')

    def _make_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_GET(self):
        if self.path == '/node_data.json':
            with open(self.data_path,'rb') as fh:
                self._make_headers()
                self.wfile.write(fh.read())
                fh.close()

    def do_POST(self):
        if self.path == '/stack_data.json':
            length = self.headers['content-length']
            data = self.rfile.read(int(length))
            
            data_object = json.loads(data)
            base_object = 0
            
            with open(self.edit_path, 'rb') as fh_in:
                base_object = json.loads(fh_in.read())
            
            base_object["nodes"][(data_object["list_id"])]["values"] = data_object["data"]["values"]
            new_data = json.dumps(base_object)
            
            with open(self.edit_path, 'w') as fh_out:
                fh_out.write(new_data)

            self.send_response(200)
            self.send_header('Received', 'OK')
            self.end_headers()
        
def run(server=HTTPServer, handler=Server, port=8008):
    url = ('', port)
    http_server = server(url, handler)
    
    print('Starting http-server on port %d...' % port)
    http_server.serve_forever()
    
if __name__ == "__main__":
        run()

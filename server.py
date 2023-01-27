#  coding: utf-8 
import socketserver
import os


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data = self.data.decode("utf-8")
        self.data = self.data.split(" ")
        if self.data[0] == 'GET':
            self.get_method()
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))
    def get_method(self):
        data_ = self.data[1]

        # check if path ends with '/'
        if not data_.endswith('/'):
            # redirect to correct path
            self.redirect_path(data_)
            return

        # check file extension
        ext = self.get_file_extension(data_)
        content_type = self.get_content_type(ext)
        if content_type is None:
            self.send_404()
            return

        # send file
        self.send_file(data_, content_type)
    
    def redirect_path(self, path):
        location = path + '/'
        message = "HTTP/1.1 301 Moved Permanently\r\n" + "Location: " + location + "\r\n"
        self.request.sendall(bytearray(message, 'utf-8'))

    def get_file_extension(self, path):
        ext = path.split('.')[-1]
        return ext
    
    def get_content_type(self, ext):
        content_types = {
            'html': 'text/html',
            'css': 'text/css',
        }
        return content_types.get(ext)
    
    # def send_404(self):
    #     message = "HTTP/1.1 404 Not Found\r\n"
    #     self.request.sendall(bytearray(message, 'utf-8'))
    
    # def send_file(self, path, content_type):
    #     try:
    #         # read file
    #         with open(path, 'r') as f:
    #             content = f.read()

    #         # send headers
    #         headers = "HTTP/1.1 200 OK\n" + "Content-Type: " + content_type + "\n" + "Content-Length: " + str(len(content)) + "\r\n\r\n"
    #         self.request.send(headers.encode())

    #         # send content
    #         self.request.send(content.encode())
    #     except:
    #         self.send_404()
    def send_file(self, path, content_type):
        try:
            # read file
            with open(path, 'r') as f:
                content = f.read()

            # send headers
            headers = "HTTP/1.1 200 OK\n" + "Content-Type: " + content_type + "\n" + "Content-Length: " + str(len(content)) + "\r\n\r\n"
            self.request.send(headers.encode())

            # send content
            self.request.send(content.encode())
        except FileNotFoundError:
            self.send_404()
        except PermissionError:
            self.send_403()
        
    def send_404(self):
        message = "HTTP/1.1 404 Not Found\r\n"
        self.request.sendall(bytearray(message, 'utf-8'))

    def send_403(self):
        message = "HTTP/1.1 403 Forbidden\r\n"
        self.request.sendall(bytearray(message, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


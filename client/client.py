from socket import socket
import json

from graphic import init_graphic

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket()
        self.running = False

    def start(self):
        self.socket.connect((self.host, self.port))

    def stop(self):
        self.running = False
        self.socket.close()

    def send(self, data):
        data=json.dumps(data).encode()
        self.socket.sendall(data)

    def receive(self):
        data = self.socket.recv(1024)

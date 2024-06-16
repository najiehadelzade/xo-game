from socket import socket
from threading import Thread

from player import Player
from game import Game

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.connections = []
        self.threads = []
        self.running = True
        self.players = []
        self.games = []

    def start(self):
        while self.running:
            print("SERVER: Waiting for connections...")
            conn, addr = self.socket.accept()
            print("SERVER: Connection from: " + str(addr))
            self.connections.append(conn)
            thread = Thread(target=self.handle, args=(conn, addr))
            self.threads.append(thread)
            thread.start()

    def handle(self, conn, addr):
        player = Player("najieh khak barsar", conn, addr)
        if self.players and self.players[-1].ready == True:
            game = Game(len(self.games), player, self.players[-1])
            self.games.append(game)
            game.play()
        else:
            conn.sendall(b'Wait for another player\n')
        self.players.append(player)


        # try:
        #     while self.running:
        #         # TODO: Handle client requests
        #         data = conn.recv(1024)
        #         conn.send(data)

        # except Exception as e:
        #     print(e)
        #     print("SERVER: Connection closed: " + str(addr))
        #     self.connections.remove(conn)
        #     self.threads.remove(Thread(target=self.handle, args=(conn, addr)))
        #     conn.close()

    def stop(self):
        self.running = False
        for conn in self.connections:
            conn.close()
        for thread in self.threads:
            thread.join()
        self.socket.close()

    def send_all(self, data):
        for conn in self.connections:
            conn.send(data)

    def get_connections(self):
        return self.connections

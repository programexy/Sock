import socket
from _thread import start_new_thread
import sys
import pickle
# from client import Bullet
import pygame.math

from settings import *
import random
# import asyncio

class Server:
    def __init__(self):
        self.host = host
        self.port = port
        self.starter_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.starter_socket.bind((self.host, self.port))
        except socket.error as error:
            print(str(error))

        self.starter_socket.listen(2)
        print('Socket is listening :)')
        self.response = ':)'
        self.clients_id = 0
        self.clients = {}
        self.generate_chaser_id = True
        self.chaser = None


    def generate_chaser(self):
        self.chaser = random.randint(0, len(self.clients.keys()) - 1)
        self.generate_chaser_id = False




    def client_thread(self, connection, client_id):
        # objects = {'hi':'msg','wassup':'msg'}
        connection.send(str.encode(str(client_id)))
        print('New client joined! here is the id: ', client_id)

        while True:
            try:
                data = connection.recv(byte_limit)
                self.response = pickle.loads(data)
                chaser_id = False

                if not data:
                    print('Sorry no data is received')
                    print('Disconnecting')
                    break

                else:
                    # print('Received:', self.response)
                    if self.chaser == client_id:
                        chaser_id = True
                    self.clients[self.response['id']] = {'position': self.response['position'],
                                                           'chaser_id': chaser_id,
                                                         'id': client_id,
                                                         'rect':self.response['rect'],
                                                         'bullets':self.response['bullets']}

                connection.sendall(pickle.dumps(self.clients))

            except Exception as error:
                print('Sorry something went wrong, here is the error: \n', error)
                break

        # self.clients
        print(self.clients)
        self.clients.pop(str(client_id))

        print('Lost connection')
        connection.close()

    def run(self):
        while True:
            connection, address = self.starter_socket.accept() # needs to always accept connection
            if len(self.clients.keys()) > 1:
                if self.generate_chaser_id:
                    self.generate_chaser()
                    self.generate_chaser_id = False
            print('Connected to:', address)
            start_new_thread(self.client_thread, (connection, self.clients_id))
            self.clients_id += 1


if __name__ == '__main__':
    server = Server()
    server.run()
    
import socket
import os

class Socket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connect()

    def verify(self):
        if not self.ip or not self.port:
            raise Exception("Cannot connect to socket, IP or Port null")
        try:
            self.port = int(self.port)
            if not self.port:
                raise Exception("Bad port")
        except Exception as e:
            print("Error occurred: {}".format(e))

    def connect(self):
        self.verify()
        connection = (self.ip, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to {0}".format(connection))
        try:
            self.sock.connect(connection)
            self.connected = True
        except Exception as e:
            print("Error occurred while connecting {}".format(e))
            self.connected = False
        finally:
            return self.connected

    def send(self, message_size, data):
        self.sock.sendall(message_size + data)
import threading

import socket
from time import sleep

from utils.constants import SOCKET_RETRY_DELAY


class Socket:
    def __init__(self, ip, port):
        self.connected = False
        self.sock = None
        self.ip = ip
        self.port = port
        self.heartbeat = None

    def verify(self):
        if not self.ip or not self.port:
            raise Exception("Cannot connect to socket, IP or Port null")
        try:
            self.port = int(self.port)
            if not self.port:
                raise Exception("Bad port")
        except Exception as e:
            print("Error occurred: {}".format(e))

    def is_alive(self):
        while True:
            try:
                self.sock.sendall(b"")
                self.connected = True
            except:
                if self.connected:
                    print("Lost connection to server")
                self.connected = False
            finally:
                print("Connection status: {}".format("Connected" if self.connected else "Not connected"))
                sleep(SOCKET_RETRY_DELAY)

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
            self.setup_heartbeat()
            return self.connected

    def send(self, message_size, data):
        self.sock.sendall(message_size + data)

    def setup_heartbeat(self):
        if not self.heartbeat:
            self.heartbeat = threading.Thread(target=self.is_alive)
        self.heartbeat.start()

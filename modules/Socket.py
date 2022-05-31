import sys
import threading

import socket
from time import sleep
from utils.Log import Log

from utils.constants import SOCKET_RETRY_DELAY


class Socket:
    def __init__(self, ip, port):
        self.connected = False
        self.sock = None
        self.ip = ip
        self.port = port
        self.heartbeat = None
        self.log = Log(type(self).__name__)

    def verify(self):
        try:
            if not self.ip or not self.port:
                raise Exception("IP or Port null")
            self.port = int(self.port)
        except ValueError as ve:
            self.log.critical("Bad port: {}".format(ve))
            sys.exit(0)
        except Exception as e:
            self.log.critical("Bad server address: {}".format(e))
            sys.exit(0)

    def is_alive(self):
        while True:
            try:
                if not self.connected:
                    self.connect()
                self.sock.sendall(b"")
                self.connected = True
            except socket.error:
                if self.connected:
                    self.log.error("Lost connection to server")
                self.connected = False
            finally:
                self.log.info("Connection status: {}".format("Connected" if self.connected else "Not connected"))
                sleep(SOCKET_RETRY_DELAY)

    def connect(self):
        self.verify()
        connection = (self.ip, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log.info("Connecting to {0}".format(connection))
        try:
            self.sock.connect(connection)
            self.connected = True
        except Exception as e:
            self.log.error("Error occurred while connecting {}".format(e))
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

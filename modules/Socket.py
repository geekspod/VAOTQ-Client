import json
import sys
import threading

import socket
from time import sleep
from utils.Log import Log

from utils.constants import SOCKET_RETRY_DELAY


class Socket:
    def __init__(self, ip, port):
        self.on_receive_callbacks = []
        self.connected = False
        self.is_command = None
        self.command_handler = None
        self.sock = None
        self.ip = ip
        self.port = port
        self.heartbeat = None
        self.receiver = None
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
            self.setup_receiver(forced=True)
        except Exception as e:
            self.log.error("Error occurred while connecting {}".format(e))
            self.connected = False
        finally:
            if not self.heartbeat:
                self.setup_heartbeat()
            if not self.receiver:
                self.setup_receiver()
            return self.connected

    def send(self, message_size, data):
        try:
            self.sock.sendall(message_size + data)
        except ConnectionResetError as cre:
            self.log.error("Disconnected from server: {}".format(cre))
            self.connected = False

    def on_receive(self):
        while self.connected:
            try:
                data = self.sock.recv(1024).decode()
                data = json.loads(data)
                if self.is_command(data):
                    self.command_handler(data)
                else:
                    for cb in self.on_receive_callbacks:
                        cb(data)
            except ConnectionResetError as cre:
                self.log.error("Disconnected from server: {}".format(cre))
                self.connected = False

    def setup_heartbeat(self):
        if not self.heartbeat:
            self.heartbeat = threading.Thread(target=self.is_alive)
        self.heartbeat.start()

    def setup_receiver(self, forced=False):
        if not self.receiver or forced:
            self.receiver = threading.Thread(target=self.on_receive)
        self.receiver.start()

    def set_is_command(self, fn):
        self.is_command = fn

    def set_command_handler(self, fn):
        self.command_handler = fn


import os
import pickle
import socket
import struct

import cv2


cap = cv2.VideoCapture(0)

connection = (os.environ['ip'], int(os.environ['port']))

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Connecting to {0}".format(connection))

clientsocket.connect(connection)



while True:

    ret, frame = cap.read()

    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

    data = pickle.dumps(frame)

    message_size = struct.pack("L", len(data))

    clientsocket.sendall(message_size + data)

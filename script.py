import os
import pickle
import socket
import struct

import cv2

from video import Video

video_stream = Video()
video_stream.start()

connection = (os.environ['ip'], int(os.environ['port']))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to {0}".format(connection))

sock.connect(connection)

while True:

    frame = cv2.resize(video_stream.frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

    data = pickle.dumps(frame)

    message_size = struct.pack("L", len(data))

    sock.sendall(message_size + data)

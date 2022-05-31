import os
import pickle
import socket
import struct

import cv2

from video import Video
from socket import Socket

video_stream = Video()
video_stream.start()

socket = Socket(os.environ['ip'], int(os.environ['port']))

if socket.connect() == False:
    raise Exception("Error occurred while connecting")

while socket.connected:
    frame = cv2.resize(video_stream.frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))
    socket.send(message_size, data)

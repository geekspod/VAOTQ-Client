import pickle
import struct
import cv2

from utils.constants import SOCKET_RETRY_DELAY


class Client:
    def __init__(self, video, socket):
        self.video = video
        self.socket = socket

    def start_video(self):
        self.video.start()

    def connect_socket(self):
        if not self.socket.connect():
            print("Could not connect to socket, will retry after {} seconds".format(SOCKET_RETRY_DELAY))

    @staticmethod
    def preprocess_video_frame(frame):
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        data = pickle.dumps(frame)
        message_size = struct.pack("L", len(data))
        return message_size, data

    def send_data(self, size, data):
        self.socket.send(size, data)

    def start(self):
        self.start_video()
        self.connect_socket()
        self.video.on_frame_change = self.on_frame_change

    def on_frame_change(self, frame):
        if not self.socket.connected:
            return
        size, data = self.preprocess_video_frame(frame)
        self.send_data(size, data)

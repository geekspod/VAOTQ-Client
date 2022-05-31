import pickle
import struct
import cv2

from utils.constants import SOCKET_RETRY_DELAY


class Client:
    def __init__(self, video, socket):
        self.video = video
        self.socket = socket
        self.start_video()
        self.connect_socket()

    def start_video(self):
        self.video.start()

    def connect_socket(self):
        if not self.socket.connect():
            print("Could not connect to socket, will retry after {} seconds".format(SOCKET_RETRY_DELAY))

    def get_video_frame(self):
        return self.video.frame

    @staticmethod
    def preprocess_video_frame(frame):
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        data = pickle.dumps(frame)
        message_size = struct.pack("L", len(data))
        return message_size, data

    def send_data(self, size, data):
        self.socket.send(size, data)

    def start(self):
        while self.socket.connected:
            frame = self.get_video_frame()
            size, data = self.preprocess_video_frame(frame)
            self.send_data(size, data)

import pickle
import struct
import cv2

from utils.Log import Log
from utils.constants import SOCKET_RETRY_DELAY, IMAGE_RESIZE


class Client:
    def __init__(self, video, socket, actuators, controller):
        self.video = video
        self.socket = socket
        self.actuators = actuators
        self.controller = controller
        self.log = Log(type(self).__name__)

    def start_video(self):
        self.video.start()

    def connect_socket(self):
        if not self.socket.connect():
            self.log.warning("Could not connect to socket, will retry after {} seconds".format(SOCKET_RETRY_DELAY))

    @staticmethod
    def preprocess_video_frame(frame):
        frame = cv2.resize(frame, None, fx=IMAGE_RESIZE, fy=IMAGE_RESIZE, interpolation=cv2.INTER_CUBIC)
        data = pickle.dumps(frame)
        message_size = struct.pack("L", len(data))
        return message_size, data

    def send_data(self, size, data):
        self.socket.send(size, data)

    def start(self):
        self.start_video()
        self.connect_socket()
        self.setup_callbacks()

    def setup_callbacks(self):
        self.socket.on_receive_callbacks += [self.on_coordinates_update]
        self.video.on_frame_change += [self.on_frame_change]
        self.socket.is_command = self.controller.is_valid_command
        self.socket.command_handler = self.controller.handle_command

    def on_frame_change(self, frame):
        if not self.socket.connected:
            return
        size, data = self.preprocess_video_frame(frame)
        self.send_data(size, data)

    def on_coordinates_update(self, coordinates):
        self.actuators.set_command(coordinates)

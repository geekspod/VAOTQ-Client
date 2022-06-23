import os

from modules import Actuators, Client, Socket, Video, Controller


def main():
    video_stream = Video()
    sock = Socket(os.environ['ip'], os.environ['port'])
    actuators = Actuators()
    controller = Controller()
    client = Client(video_stream, sock, actuators, controller)
    client.start()


if __name__ == "__main__":
    main()

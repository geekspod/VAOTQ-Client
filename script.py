import os

from modules import Actuators, Client, Socket, Video


def main():
    video_stream = Video()
    sock = Socket(os.environ['ip'], os.environ['port'])
    actuators = Actuators()
    client = Client(video_stream, sock, actuators)
    client.start()


if __name__ == "__main__":
    main()

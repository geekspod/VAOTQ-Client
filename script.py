import os

from modules import Client, Socket, Video


def main():
    video_stream = Video()
    sock = Socket(os.environ['ip'], os.environ['port'])
    client = Client(video_stream, sock)
    client.start()


if __name__ == "__main__":
    main()

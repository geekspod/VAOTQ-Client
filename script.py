import os

from modules import Client, Socket, Video

video_stream = Video()

sock = Socket(os.environ['ip'], int(os.environ['port']))


client = Client(video_stream, sock)

client.start()

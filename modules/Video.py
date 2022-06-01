import cv2
import threading


class Video:
    def __init__(self, video_path=0):
        self.on_frame_change = []
        self.video = cv2.VideoCapture(video_path)
        self.frame = None
        self.running = False
        self.thread = None

    def video_feed(self):
        while self.running:
            ret, frame = self.video.read()
            self.frame = frame
            if len(self.on_frame_change):
                for fn in self.on_frame_change:
                    fn(frame)
            if not ret:
                raise Exception("Video Failure")
        return True

    def start(self):
        if not self.thread:
            self.thread = threading.Thread(target=self.video_feed)
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.frame = None
        self.video.release()
        self.thread.join()
        self.thread = None
        return True

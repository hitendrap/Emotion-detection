import cv2
import threading
import os

thread = None
cascPath = os.path.dirname(cv2.__file__) + \
"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


class Camera:
    def __init__(self, fps=30, video_source=0):
        self.fps = fps
        self.video_source = video_source
        self.camera = cv2.VideoCapture(self.video_source)
        self.max_frames = 5*self.fps
        self.frames = []
        self.isrunning = False

    def run(self):
        global thread
        if thread is None:
            thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.isrunning = True
            thread.start()

    def _capture_loop(self):
        dt = 1/self.fps
        while self.isrunning:
            v, im = self.camera.read()
            grayFrame = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                grayFrame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            if v:
                if len(self.frames) == self.max_frames:
                    self.frames = self.frames[1:]
                self.frames.append(grayFrame)
                for (x, y, w, h) in faces:
                    cv2.rectangle(grayFrame, (x, y),
                                  (x+w, y+h), (0, 255, 0), 2)

    def stop(self):
        self.isrunning = False

    def get_frame(self, _bytes=True):
        if len(self.frames) > 0:
            if _bytes:
                img = cv2.imencode('.png', self.frames[-1])[1].tobytes()
            else:
                img = self.frames[-1]
        else:
            with open("images/main.png", "rb") as f:
                img = f.read()
        return img

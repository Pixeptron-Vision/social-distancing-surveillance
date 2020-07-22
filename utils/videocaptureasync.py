# file: videocaptureasync.py
from threading import Thread
import cv2

class VideoCaptureAsync:
    def __init__(self, src=0):
        self.src = src
        try:
            self.cap = cv2.VideoCapture(self.src)
        except cv2.error as err:
            self.cap = None
        # if(self.cap is not None):
        #     self.grabbed, self.frame = self.cap.read()
        self.grabbed=False
        self.frame=None
        self.started = False
        #self.read_lock = threading.Lock()

    def isOpened(self):
        if self.cap is not None:
            return self.cap.isOpened()
        else:
            return False
        

    def start(self):
        if self.started or self.cap is None:
            return self
        self.started = True
        self.thread = Thread(target=self.update,name='frame_grabber_thread',args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        while not self.isOpened():
            self.cap.release()
            try:
                self.cap = cv2.VideoCapture(self.src)
            except cv2.error as err:
                self.cap = None

        while self.started :
            grabbed, frame = self.cap.read()
            self.grabbed = grabbed
            self.frame = frame
            if self.grabbed==False or self.isOpened()==False:
                self.cap.release()
                self.cap = cv2.VideoCapture(self.src)
                cv2.waitKey(1000)


    def read(self):
        return self.grabbed, self.frame

    def stop(self):
        self.started = False
        if self.cap is not None:
            self.cap.release()
#         self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()

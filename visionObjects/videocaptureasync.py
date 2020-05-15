# file: videocaptureasync.py
from threading import Thread
import cv2

class VideoCaptureAsync:
    def __init__(self, src=0):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        #self.read_lock = threading.Lock()

    def isOpened(self):
        return self.cap.isOpened()

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        if self.started:
            print('[!] Asynchroneous video capturing has already been started.')
            return None
        self.started = True
        self.thread = Thread(target=self.update,name='frame_grabber_thread',args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        while not self.cap.isOpened():
            self.cap.release()
            self.cap = cv2.VideoCapture(self.src)
        while self.started :
            grabbed, frame = self.cap.read()
            self.grabbed = grabbed
            self.frame = frame
            if self.grabbed==False or self.isOpened()==False:
                self.cap.release()
                self.cap = cv2.VideoCapture(self.src)
                cv2.waitKey(1000)


    def read(self):
#         with self.read_lock:
#         if self.frame is not None:
#             frame = self.frame
#         else:
#             frame = None
#         grabbed = self.grabbed
        return self.grabbed, self.frame

    def stop(self):
        self.started = False
        self.cap.release()
#         self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()

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
        while self.started and self.cap.isOpened():
            try:
                grabbed, frame = self.cap.read()
#             with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame
            except cv2.error as err:
                print(err)
                self.stop()
                break

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
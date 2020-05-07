
from threading import Thread
import cv2
import time
import sys
import multiprocessing

class TimeoutThread:
    def __init__(self,camera):
        self.stopped = False
        self.cap = camera
    def start(self):
        # self.timer_thread = multiprocessing.Process(target=self.runTimer,args=())
        self.timer_thread = Thread(target=self.runTimer,args=())
        self.timer_thread.daemon = True
        self.timer_thread.start()
        self.stopped=False
    def stop(self):
        self.stopped=True

    def runTimer(self):
        while (self.stopped==False):
            time.sleep(1)
            print('sleep_over')
            if(ret==False and prev_ret==True):
                print("Camera is disconnected!")
                self.stopped=True
                self.cap.stop()
                # self.timer_thread.terminate()
                display_stream_error(self.camera)
                break
    def __exit__(self, exec_type, exc_value, traceback):
        self.stopped=True





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
    # def start_count(self):
    #     self.timer_thread = Thread(target=self.runTimer,name='read_timeout',args=())
    #     self.timer_thread.daemon = True
    #     self.timer_thread.start()

    # def runTimer(self):
    #     time.sleep(3)
    #     print('sleep_over')
    #     if(self.grabbed==False):
    #         self.stop()
    #         return False,None

    def update(self):
        i=0
        while self.started and self.cap.isOpened():
            i+=1
            try:
                # self.grabbed=False
                # self.frame=None
                # self.start_count()
                beg = time.time()
                grabbed, frame = self.cap.read()
                print(i," ",time.time()-beg)
#             with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame
            except cv2.error as err:
                print(err)
                self.stop()
                break

    def read(self):
#         with self.read_lock:
        return self.grabbed, self.frame

    def stop(self):
        self.started = False
        self.cap.release()
#         self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()






ret = False
prev_ret = False
def display_captured_stream(camera):
    cv2.destroyWindow('Error')    # Destroy the error window if stream was unavailable earlier.
    while True:
        ret = False
        t = TimeoutThread(camera)
        t.start()
        ret, image = camera.read()
        prev_ret=ret
        t.stop()
        if not ret or image is None:
            print("Camera is disconnected!")
            camera.stop()
            return False
        else:
            image = cv2.resize(image, (500,500), interpolation=cv2.INTER_AREA)
            cv2.imshow('Cam Stream', image)           # Display the stream if available

        if cv2.waitKey(1) & 0xFF == 27:
            camera.stop()
            cv2.destroyAllWindows()
            sys.exit(0)                        # Pressing ESC key exits the program
            break

    return True


# Function for error display if stream is unavailable at start or camera port is inaccessible.
def display_stream_error(camera):
    camera.stop()
    cv2.destroyWindow('Cam Stream')
    error_img = cv2.imread('.\stream_error.jpg')
    error_img = cv2.resize(error_img, (500,500), interpolation=cv2.INTER_AREA)
#     print('Camera disconnected')
    cv2.imshow('Error',error_img)
    cv2.waitKey(3000)                 # A 3 second refresh/halt to recheck connections



cv2.namedWindow('Cam Stream')
while True:
    camera = VideoCaptureAsync(0)
    camera.start()
    if camera.isOpened():
        print('Camera is connected')

        response = display_captured_stream(camera)
        if response == False:
            display_stream_error(camera)
            continue
    else:                                # If system is unable to open/access the camera port.
        display_stream_error(camera)
        continue

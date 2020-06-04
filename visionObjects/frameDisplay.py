# file: videocaptureasync.py
from threading import Thread
import cv2


class FrameDisplay:

    def __init__(self):
        self.stream = None
        self.started = False
        error = cv2.imread('stream_error.jpg')
        error = cv2.resize(error, (300, 300))
        self.error_image = error
        self.user_exit = False

        # cv2.namedWindow("Stream", cv2.WINDOW_AUTOSIZE)
        #self.read_lock = threading.Lock()

    def start(self):
        if self.started:
            print('[!] Frame display has already been started.')
            return None
        self.started = True
        self.thread = Thread(target=self.display, name='GUI_thread', args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def display(self):
        while self.started:
            # Displaying the frames
            if self.stream is not None:
                cv2.imshow("Stream", self.stream)
            else:
                cv2.destroyWindow('Stream')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                self.user_exit = True
                # sys.exit(0)
                break

    # def update(self, frame1=None, activity_frame, mean_background_frame, motion_frame, act_frame_diff, static_motion_frame):
    def update(self, frame1=None,):
        self.stream = frame1
        return self.user_exit

    def display_error(self):
        self.stream = self.error_image
        return self.user_exit

    def stop(self):
        self.started = False
        cv2.destroyAllWindows()

    def __exit__(self, exec_type, exc_value, traceback):
        cv2.destroyAllWindows()

# file: videocaptureasync.py
from threading import Thread
import cv2


class FrameDisplay:
    # def __init__(self,stream=None,motion=None,background=None):
    def __init__(self):
        self.stream = None
        self.motion = None
        self.background = None
        self.act_frame_diff = None
        self.static_motion_frame = None
        self.started = False
        error = cv2.imread('stream_error.jpg')
        error = cv2.resize(error, (640, 480))
        self.error_image = error
        self.user_exit = False
        self.index=1
        # cv2.namedWindow("Stream", cv2.WINDOW_AUTOSIZE)
        # cv2.namedWindow("Motion", cv2.WINDOW_AUTOSIZE)
        # cv2.namedWindow("Background", cv2.WINDOW_AUTOSIZE)

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
                cv2.imshow(str(self.index), self.stream)
            else:
                cv2.destroyWindow(str(self.index))
            if self.motion is not None:
                cv2.imshow("Activity Detection", self.motion)
            else:
                cv2.destroyWindow('Motion')

            # Displaying median background frame
            if self.background is not None:
                cv2.imshow("Background", self.background)
            else:
                cv2.destroyWindow('Background')

            if self.act_frame_diff is not None:
                cv2.imshow("act_frame_diff", self.act_frame_diff)
            else:
                cv2.destroyWindow('act_frame_diff')

            if self.static_motion_frame is not None:
                cv2.imshow("static_motion_frame", self.static_motion_frame)
            else:
                cv2.destroyWindow('static_motion_frame')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                self.user_exit = True
                # sys.exit(0)
                break

    def update(self, frame1, threst_delta, mean_background_frame, act_frame_diff, static_motion_frame):
        self.stream = frame1
        self.motion = threst_delta
        self.background = mean_background_frame
        self.act_frame_diff = act_frame_diff
        self.static_motion_frame = static_motion_frame
        return self.user_exit

    def display_error(self):
        self.stream = self.error_image
        self.motion = None
        self.background = None
        return self.user_exit

    def stop(self):
        self.started = False
        cv2.destroyAllWindows()

    def __exit__(self, exec_type, exc_value, traceback):
        cv2.destroyAllWindows()

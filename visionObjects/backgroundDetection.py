import cv2
import numpy as np
from threading import Thread


class background:
    mean_background_frame = None
    previous_background_frame = None
    static_motion_frame = None
    previous_frame = None
    motion_frame = None
    current_frame = None
    background_reference = None
    motion_status = False
    started = False
    # Constructor of background Object

    def __init__(self, initial_frame=None):
        # initial_frame = cv2.resize(initial_frame, (640, 480))
        initial_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
        self.previous_background_frame = initial_frame
        self.mean_background_frame = initial_frame
        self.static_motion_frame = self.update_static_motion(
            self.mean_background_frame, self.previous_background_frame)
        self.previous_frame = initial_frame
        # For background reference
        self.background_reference = initial_frame

    def start(self):
        if self.started:
            print('[!] Background Update is running')
            return None
        self.started = True
        self.thread = Thread(target=self.update_background,
                             name='BU_thread', args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    # def back_append_thread(self,current_frame):
    #     self.current_frame = current_frame
    #     self.fid += 1
    #
    #     append_thread = Thread(target=self.background_filter,args=())
    #     append_thread.start()
    #     return append_thread

    # Method to determine static frames
    def background_filter(self, current_frame=None):
        # motion_status = self.motion_status #Not needed/Extra variable
        previous_frame = self.previous_frame
        if current_frame is not None:
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            self.current_frame = current_frame

        # Resizing the frame
        # current_frame = cv2.resize(current_frame, (640, 480))
        # previous_frame = cv2.resize(previous_frame, (640, 480))
        # Applying appropiate filters
        frame_diff = cv2.absdiff(self.current_frame, previous_frame)
        #gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        gray = frame_diff
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        threst_delta = cv2.threshold(
            blur, 10, 255, cv2.THRESH_BINARY)[1]
        self.motion_frame = threst_delta
        # Currently no dilation
        kernel = np.ones((9, 9), np.uint8)
        threst_delta = cv2.morphologyEx(threst_delta, cv2.MORPH_CLOSE, kernel)
        erosion = cv2.erode(threst_delta, kernel, iterations=0)
        dilated = cv2.dilate(erosion, kernel, iterations=3)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Checking for motion frame
        motion_status = not self.is_static_frame(contours)
        # If the frame is not motion frame/ is static frame
        if not motion_status:
            self.recalculate_ref(self.current_frame)
        # To ensure subsequent frame comparision
        self.previous_frame = self.current_frame

    def is_static_frame(self, contours):
        for cnt in contours:
            # filtering out all noise contours to ignore
            if cv2.contourArea(cnt) < 500:
                continue
        # If motion contours are present, return True
            return False
        # After checking the contours,
        # If motion contours are absent, return False
        return True

    def recalculate_ref(self, frame):
        # New implementation
        background_reference_copy = self.background_reference
        # Convertion to float for rudimentary operations
        frame = frame.astype(float)
        background_reference_copy = background_reference_copy.astype(float)
        alpha = 0.7
        new_background_reference = alpha * \
            background_reference_copy + (1-alpha)*frame
        new_background_reference = np.round(new_background_reference)
        # Saving the new reference
        self.background_reference = np.uint8(new_background_reference)

    def update_background(self, fps=15, threshold_time_frame=40):
            # Saving new previous background frame itself
        self.previous_background_frame = self.mean_background_frame
        # Saving new background frame
        self.mean_background_frame = self.background_reference
        self.static_motion_frame = self.update_static_motion(
            self.mean_background_frame, self.previous_background_frame)

    def get_background_frame(self):
        return self.mean_background_frame

    def update_static_motion(self, curr_background, prev_background):
        #curr_background = cv2.cvtColor(curr_background, cv2.COLOR_BGR2GRAY)
        #prev_background = cv2.cvtColor(prev_background, cv2.COLOR_BGR2GRAY)
        return cv2.absdiff(curr_background, prev_background)

    def get_static_motion_frame(self):
        return self.static_motion_frame

    def get_motion_frame(self):
        return self.motion_frame

    def stop(self):
        self.started = False

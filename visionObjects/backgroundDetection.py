import cv2
import numpy as np
from threading import Thread

class background:

    # Constructor of background Object
    def __init__(self, initial_frame=None):
        # initial_frame = cv2.resize(initial_frame, (640, 480))
        self.mean_background_frame = initial_frame
        self.previous_frame = initial_frame
        self.motion_frame = None
        self.current_frame = None
        self.static_frames = {}
        self.motion_status = False
        self.started = False
        self.fid = 0
        self.append_static_frame(initial_frame, self.fid)

    def start(self):
            if self.started:
                print('[!] Background Update is running')
                return None
            self.started = True
            self.thread = Thread(target=self.update_background,name='BU_thread',args=())
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
    def background_filter(self,current_frame=None):
        # motion_status = self.motion_status #Not needed/Extra variable
        previous_frame = self.previous_frame
        if current_frame is not None:
            self.current_frame = current_frame
            self.fid += 1

        # Resizing the frame
        # current_frame = cv2.resize(current_frame, (640, 480))
        # previous_frame = cv2.resize(previous_frame, (640, 480))
        # Applying appropiate filters
        frame_diff = cv2.absdiff(self.current_frame, previous_frame)
        gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        threst_delta = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)[1]
        self.motion_frame = threst_delta
        # Currently no dilation
        dilated = cv2.dilate(threst_delta, None, iterations=0)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Checking for motion frame
        motion_status = self.is_static_frame(contours)
        # If the frame is not motion frame/ is static frame
        if not motion_status:
            self.append_static_frame(self.current_frame, self.fid)
        # To ensure subsequent frame comparision
        self.previous_frame = self.current_frame



    def is_static_frame(self, contours):
        for cnt in contours:
            # filtering out all noise contours to ignore
            if cv2.contourArea(cnt) < 500:
                continue
        # If motion contours are present, return True
            return True
        # After checking the contours,
        # If motion contours are absent, return False
        return False

    def append_static_frame(self, frame, fid):
        self.static_frames[fid] = frame


    def update_background(self, fps=15, threshold_time_frame=40):
        while self.started:
            # if no of frames in static_frames > threshold no of frames to update
            if len(self.static_frames) > fps * threshold_time_frame:
                # Taking the mean of background frames using the frame id
                static_frames_ids = []
                for i in sorted(self.static_frames.keys()):
                    static_frames_ids.append(i)
                np_static_frames_ids = np.array(static_frames_ids)
                # mean frame id of background
                mean_id = int(np.mean(np_static_frames_ids))
                np_static_frames_ids = np_static_frames_ids[np_static_frames_ids >= mean_id]
                # mean background frame itself
                self.mean_background_frame = self.static_frames[np_static_frames_ids[0]]
                # Clearing background list and appending new background to it
                self.clear_static_frames()

    def get_background_frame(self):
        return self.mean_background_frame

    def get_motion_frame(self):
        return self.motion_frame

    def clear_static_frames(self):
        self.static_frames.clear()

        self.fid = 0
        self.append_static_frame(self.mean_background_frame, self.fid)
    def stop(self):
        self.started=False

import numpy as np
import argparse
import cv2
import imutils
import sys
from scipy.spatial import distance
import datetime as dt
import time
from threading import Thread
from multiprocessing import Process
# VideoCaptureAsync implements separate thread for reading stream from camera
from visionObjects.videocaptureasync import VideoCaptureAsync
from visionObjects.frameDisplay import FrameDisplay
from visionObjects.distanceCalc import calculate_dist
from visionObjects.backgroundDetection import background
#from visionObjects.streamError import display_stream_error
from visionObjects.activityDetection import activity_filter, calc_centers


class VisionSurveillance:

    def __init__(self,src=0):
        self.src = src;

        self.timeDuration = dt.timedelta(seconds=20)
        self.desired_time_frame = int(self.timeDuration.seconds)
        #desired_time_frame = 10
        self.frame_rate = 15
        self.threshold_dist = 75
        # For background frame, intialising a background_frames dictionary
        self.background_frames = {}
        self.motion_status = False
        self.mean_background_frame = None

    # def start(self):
    #     # self.display_obj = FrameDisplay().start()
    #     # self.display_obj.index=index_count
    #     # self.cap = VideoCaptureAsync(src=self.src).start()
    #     # self.backUpdate_obj = background()
    #     self.started=True
    #     return self


    def initialize_first_frame(self):
        ret,frame = self.cap.read()
        # frame = cv2.imread('stream_error.jpg')
        if frame is None:
            print("[INFO] Stream unavailable..!")
            user_exit = display_obj.display_error()
        else:
            self.fid = 1
            frame = cv2.resize(frame, (640, 480))
            # Set first frame as default background
            #background_frame = cv2.imread('background.jpg', 1)
            self.background_frame = frame
            # Initialize background update object and pass first frame
            self.backUpdate_obj = background(self.background_frame)
            # Set previous frame to first frmae for starting conditions
            self.prev_frame = frame

    def spawn_detection(self,index_count):
        self.started=True
        self.process = Process(target=self.detection,args=(index_count,))
        self.process.start()
#
    def detection(self,index_count):
        self.display_obj = FrameDisplay().start()
        self.display_obj.index=index_count
        self.cap = VideoCaptureAsync(src=self.src).start()
        self.initialize_first_frame()

        while self.started:

            ret, current_frame = self.cap.read()
            if not ret or current_frame is None:
                print("[INFO] Cam IP Stream unavailable...")
                user_exit = self.display_obj.display_error()

            else:
                # print("fid - ", fid)
                self.motion_status = False
                # Resizing the frame
                self.prev_frame = cv2.resize(self.prev_frame, (640, 480))
                current_frame = cv2.resize(current_frame, (640, 480))
                # back_append_thread = backUpdate_obj.back_append_thread(current_frame)

                # Update the background and append current frame if no motion
                self.backUpdate_obj.background_filter(current_frame)
                self.backUpdate_obj.update_background()

                self.background_frame = self.backUpdate_obj.get_background_frame()
                # static_motion_frame = self.backUpdate_obj.get_static_motion_frame()
                #motion_frame = backUpdate_obj.get_motion_frame()

                # Detect activity from current_frame and background_frame
                contours, (centres, boxed_current_frame), motion_frame, act_frame_diff = activity_filter(
                    current_frame, self.background_frame)
                # Returns id of pairs violating the norms
                pairs = calculate_dist(
                    boxed_current_frame, centres, self.threshold_dist)
                # Note: pairs has id index of contour center in centres list
                # persion_1_id = pairs[0] - a nx1 array
                # persion_2_id = pairs[1] - a nx1 array

                # Disaply the frames and read is user presses q/exit
                user_exit = self.display_obj.update(
                    boxed_current_frame, None,None, None,None)

                # Choosing next frame
                self.prev_frame = current_frame
                self.fid += 1

            if user_exit == True:
                self.started=False
                self.cap.stop()
                self.display_obj.stop()
                # self.process.terminate()

    def __exit__(self):
        self.cap.stop()
        self.display_obj.stop()


if __name__ == '__main__':
    #Note: index is passed in start function as indexing is important
    #       at the time of frame display...as windows are named with index
    #       to avoid mixing and overriding of frames during display.
    det1 = VisionSurveillance(src='../PNNLParkingLot2.avi')
    det2 = VisionSurveillance(src='../vid1.mp4')
    det3 = VisionSurveillance(src='../vid2.mp4')
    det4 = VisionSurveillance(src='../PNNL_Parking_LOT(1).avi')
    # det1.initialize_first_frame()
    # det2.initialize_first_frame()
    # det3.initialize_first_frame()
    # det4.initialize_first_frame()

    # li = [det1,det2,det3]
    li = [det1,det2,det3,det4]
    breaker = False

    for count,det in enumerate(li):
        det.spawn_detection(count)


    sys.exit(0)

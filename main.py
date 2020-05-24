import numpy as np
import argparse
import cv2
import imutils
import sys
from scipy.spatial import distance
import datetime as dt
import time
from threading import Thread
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

    def start(self,index_count):
        self.display_obj = FrameDisplay().start()
        self.display_obj.index=index_count
        self.cap = VideoCaptureAsync(src=self.src).start()
        # self.backUpdate_obj = background()
        return self

    # This initializes the first frmae and sets it as background and previous frame
    def initialize_first_frame(self):
        ret,frame = self.cap.read()
        if not ret or frame is None:
            print("[INFO] Stream unavailable..!")
            user_exit = self.display_obj.display_error()
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

    # This function is for detection for each frame
    def detection(self):

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
        # if user_exit == True:
        #     cap.stop()
        #     display_obj.stop()
        #     sys.exit(0)'
        return user_exit

    def __exit__(self):
        self.cap.stop()
        self.display_obj.stop()


if __name__ == '__main__':

    # cap = cv2.VideoCapture('http://service:Tata!123@192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779') #service:TATA!@123;service:Pass!234; 48.51           ;rtsp:/service:TATA!@123@192.168.48.51
    # rtsp://192.168.48.51//rtsp_tunnel , rtsp:/service:TATA!@123@192.168.48.51
    # print("Reading first frame...") #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=37660
    # ret, image = cap.read() #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779

    # Note: VideoCaptureAsync implemented here has same format as VideoCapture....just specify the link of ip cam as:
    # cap = VideoCaptureAsync(src="videofile_name / Ip camera link")



    # The below objects are the instance of VisionSurveillance visionObjects
    # and each object det is for each different cameras
    det1 = VisionSurveillance(src='../PNNLParkingLot2.avi')
    det2 = VisionSurveillance(src='../PNNL_Parking_LOT(1).avi')
    det3 = VisionSurveillance(src='../vid1.mp4')
    det4 = VisionSurveillance(src=0)
    # All four camera objects are appended in a list
    li = [det1,det2,det3,det4]

    #Note: index is passed in start function as indexing is important
    #       at the time of frame display...as windows are named with index
    #       to avoid mixing and overriding of frames during display.
    for index,obj in enumerate(li):
        obj.start(index)
        obj.initialize_first_frame()
    # breaker is used to read exit command from users
    breaker = False

    # while loop to run for each frame for all cameras for unlimited time
    while True:
        beg = time.time()
        for det in li:
            user_exit = det.detection()
            if user_exit:
                breaker=True

        print(time.time()-beg)
        # breaker checks wether the user has pressed q.
        if breaker:
            break

    sys.exit(0)

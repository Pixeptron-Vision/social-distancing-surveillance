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

from human_detector import DetectorAPI
from human_detector import centre_calcualtion

model_path = 'ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb'
detection_confidence = 0.4

class VisionSurveillance:

    def __init__(self,detectorAPI,src=0):
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
        self.odapi = detectorAPI
        self.fid=0

    def start(self,index_count):
        self.display_obj = FrameDisplay().start()
        self.display_obj.index=index_count
        self.cap = VideoCaptureAsync(src=self.src).start()
        # self.backUpdate_obj = background()
        return self

    # This function is for detection for each frame
    def detection(self):

        ret, current_frame = self.cap.read()
        if not ret or current_frame is None:
            # print("[INFO] Cam IP Stream unavailable...")
            user_exit = self.display_obj.display_error()

        else:
            # print("fid - ", fid)
            # Resizing the frame
            # current_frame = cv2.resize(current_frame, (640, 480))
            current_frame = cv2.resize(current_frame, (300, 300))

            boxes, scores, classes, num = self.odapi.processFrame(current_frame)

            centres,current_frame =centre_calcualtion(boxes,scores,classes,current_frame,detection_confidence)

            # Returns id of pairs violating the norms
            pairs = calculate_dist(
                current_frame, centres, self.threshold_dist)
            # Note: pairs has id index of contour center in centres list
            # persion_1_id = pairs[0] - a nx1 array
            # persion_2_id = pairs[1] - a nx1 array

            # Code for Anamaly Detection and Alert System
            # if (Anamaly Detection Condition) == True:
            #    safety_ok = False
            #    if unsafe_timer is None:
            #        unsafe_timer = time.time()
            #        safe_timer = None
            # else:
            #    safety_ok = True
            #    if safe_timer is None:
            #        safe_timer = time.time()
            #        unsafe_timer = None

            # if safety_ok == False:
            #    unsafety_status_msg = True
            # else:
            #    if safe_timer - time.time() >= safety_threshold_time:
            #        unsafety_status_msg = False
            #        safe_timer = time.time() #Timer is reset to recalculate after every threshold time
            #    else:
            #        unsafety_status_msg = None

            '''
            Value representation of unsafety_status_msg:
            1.If unsafety_status_msg == NONE
                This represents that the variable is reset.
                There is no unsafe condition occuring.
                Safe condition is occuring but less than threshold amount of time
            2.If unsafety_status_msg == False
                This represents that Safe condition has occured for Threshold amount of time
            3.If unsafety_status_msg == True
                This represents that Unsafe conditions are occuring right now.
            '''
            # if unsafety_status_msg is not None:
            #    if unsafety_status_msg == True:
            #        # Alert Unsafe Right Now
            #    else:
            #        # Alert Safe for one hour (Threshold time)

            # Disaply the frames and read is user presses q/exit
            user_exit = self.display_obj.update(current_frame)
            self.fid += 1

        return user_exit


    def __exit__(self):
        self.cap.stop()
        self.display_obj.stop()


if __name__ == '__main__':
    odapi = DetectorAPI(path_to_ckpt=model_path)


    # cap = cv2.VideoCapture('http://service:Tata!123@192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779') #service:TATA!@123;service:Pass!234; 48.51           ;rtsp:/service:TATA!@123@192.168.48.51
    # rtsp://192.168.48.51//rtsp_tunnel , rtsp:/service:TATA!@123@192.168.48.51
    # print("Reading first frame...") #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=37660
    # ret, image = cap.read() #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779

    # Note: VideoCaptureAsync implemented here has same format as VideoCapture....just specify the link of ip cam as:
    # cap = VideoCaptureAsync(src="videofile_name / Ip camera link")


    sources = ['rtsp://service:Tata!123@192.168.49.27/1',
                'rtsp://service:Tata!123@192.168.49.28/1',
                'rtsp://service:Tata!123@192.168.49.29/1',
                'rtsp://service:Tata!123@192.168.49.30/1',
                'rtsp://service:Tata!123@192.168.49.31/1',
                'rtsp://service:Tata!123@192.168.49.32/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1',
                'rtsp://service:Tata!123@192.168.51.5/1']
    # The below objects are the instance of VisionSurveillance visionObjects
    # and each object det is for each different cameras
    stream_objects = []
    for i in sources:
        det = VisionSurveillance(odapi,src=i)
        stream_objects.append(det)

    #Note: index is passed in start function as indexing is important
    #       at the time of frame display...as windows are named with index
    #       to avoid mixing and overriding of frames during display.
    for index,obj in enumerate(stream_objects):
        obj.start(index)
    # breaker is used to read exit command from users
    breaker = False

    # while loop to run for each frame for all cameras for unlimited time
    while True:

        for det in stream_objects:
            user_exit = det.detection()
            if user_exit:
                breaker=True
                sys.exit(0)
                # break

    sys.exit(0)

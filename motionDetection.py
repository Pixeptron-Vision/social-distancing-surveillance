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
        self.fid=0


    def spawn_detection(self,index_count):
        self.started=True
        self.process = Process(target=self.detection,args=(index_count,))
        self.process.start()
#
    def detection(self,index_count):
        self.display_obj = FrameDisplay().start()
        self.display_obj.index=index_count
        self.cap = VideoCaptureAsync(src=self.src).start()
        # self.initialize_first_frame()
        self.odapi = DetectorAPI(path_to_ckpt=model_path)

        # Safety Message Service Variables
        safety_ok = True
        unsafety_status_msg = None
        unsafe_timer = None
        safe_timer = None
        # unsafety_threshold_time = int(dt.timedelta(hours=1))
        # safety_threshold_time = int(dt.timedelta(hours=1))

        while self.started:

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

            if user_exit == True:
                self.started=False
                self.cap.stop()
                self.display_obj.stop()
                # self.process.terminate()

    def __exit__(self):
        self.cap.stop()
        self.display_obj.stop()


if __name__ == '__main__':
    #Note: index is passed in spawn function as indexing is important
    #       at the time of frame display...as windows are named with index
    #       to avoid mixing and overriding of frames during display.


    sources = ['../PNNLParkingLot2.avi',
                '../walking.avi',
                '../vid_short.mp4',
                '../PNNL_Parking_LOT(1).avi']
    # The below objects are the instance of VisionSurveillance visionObjects
    # and each object det is for each different cameras
    stream_objects = []
    for i in sources:
        det = VisionSurveillance(src=i)
        stream_objects.append(det)


    for count,det in enumerate(stream_objects):
        det.spawn_detection(count)


    sys.exit(0)

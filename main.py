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

from human_detector import DetectorAPI
from human_detector import centre_calcualtion

# The below function is responsible for implementing the Detecting the motion.
timeDuration = dt.timedelta(seconds=20)
desired_time_frame = int(timeDuration.seconds)
threshold_dist = 75
# For background frame, intialising a background_frames dictionary
motion_status = False
mean_background_frame = None



def detectMotion(cap):

    # Safety Message Service Variables
    safety_ok = True
    unsafety_status_msg = None
    unsafe_timer = None
    safe_timer = None
    # unsafety_threshold_time = int(dt.timedelta(hours=1))
    # safety_threshold_time = int(dt.timedelta(hours=1))
    fid=0
    while True:
        # Read second and subsequent frames

        ret, current_frame = cap.read()
        if not ret or current_frame is None:
            # print("[INFO] Cam IP Stream unavailable...")
            user_exit = display_obj.display_error()

        else:
            # print("fid - ", fid)
            motion_status = False
            # Resizing the frame

            current_frame = cv2.resize(current_frame, (640, 480))
            # current_frame = cv2.resize(current_frame, (1280, 720))

            boxes, scores, classes, num = odapi.processFrame(current_frame)

            centres,boxed_current_frame=centre_calcualtion(boxes,scores,classes,current_frame,prediction_confidence)
            # Returns id of pairs violating the norms
            pairs = calculate_dist(boxed_current_frame, centres, threshold_dist)
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
            user_exit = display_obj.update(boxed_current_frame)

            fid += 1
        if user_exit == True:
            cap.stop()
            display_obj.stop()
            sys.exit(0)

    cap.stop()
    display_obj.stop()
    sys.exit(0)


# Intializing and starting the UI thread object
display_obj = FrameDisplay().start()
# model_path = '/path/to/faster_rcnn_inception_v2_coco_2017_11_08/frozen_inference_graph.pb'
model_path = 'ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb'
odapi = DetectorAPI(path_to_ckpt=model_path)
prediction_confidence = 0.4



# cap = cv2.VideoCapture('http://service:Tata!123@192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779') #service:TATA!@123;service:Pass!234; 48.51           ;rtsp:/service:TATA!@123@192.168.48.51
# rtsp://192.168.48.51//rtsp_tunnel , rtsp:/service:TATA!@123@192.168.48.51
# print("Reading first frame...") #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=37660
# ret, image = cap.read() #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779

# Note: VideoCaptureAsync implemented here has same format as VideoCapture....just specify the link of ip cam as:
# cap = VideoCaptureAsync(src="videofile_name / Ip camera link")
cap = VideoCaptureAsync(src='../vid_short.mp4')
# cap = VideoCaptureAsync(src=0)
# This is responsible for starting up the thread and frame capturing process
cap.start()
while True:
    detectMotion(cap)

# cv2.destroyAllWindows()

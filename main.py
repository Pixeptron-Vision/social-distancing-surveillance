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
# The below function is responsible for implementing the Detecting the motion.
timeDuration = dt.timedelta(seconds=20)
desired_time_frame = int(timeDuration.seconds)
#desired_time_frame = 10
frame_rate = 15
threshold_dist = 75
# For background frame, intialising a background_frames dictionary
background_frames = {}
motion_status = False
mean_background_frame = None


def detectMotion(cap):

    ret, frame1 = cap.read()
    if not ret or frame1 is None:
        print("[INFO] Stream unavailable..!")
        user_exit = display_obj.display_error()
        if user_exit == True:
            cap.stop()
            display_obj.stop()
            sys.exit(0)

    else:
        fid = 1
        frame1 = cv2.resize(frame1, (640, 480))
        # Set first frame as default background
        background_frame = frame1
        # Initialize background update object and pass first frame
        backUpdate_obj = background(frame1)
        # Set previous frame to first frmae for starting conditions
        prev_frame = frame1

        print("First frame Read")

        while True:
            # Read second and subsequent frames
            beg = time.time()
            ret, current_frame = cap.read()
            if not ret or current_frame is None:
                print("[INFO] Cam IP Stream unavailable...")
                user_exit = display_obj.display_error()

            else:
                print("fid - ", fid)
                motion_status = False
                # Resizing the frame
                prev_frame = cv2.resize(prev_frame, (640, 480))
                current_frame = cv2.resize(current_frame, (640, 480))
                # back_append_thread = backUpdate_obj.back_append_thread(current_frame)

                # Update the background and append current frame if no motion
                backUpdate_obj.background_filter(current_frame)
                backUpdate_obj.update_background()

                background_frame = backUpdate_obj.get_background_frame()

                #motion_frame = backUpdate_obj.get_motion_frame()

                # Detect activity from current_frame and background_frame
                contours, (centres, boxed_current_frame), motion_frame , act_frame_diff = activity_filter(
                    current_frame, background_frame)
                # Returns id of pairs violating the norms
                pairs = calculate_dist(
                    boxed_current_frame, centres, threshold_dist)
                # Note: pairs has id index of contour center in centres list
                # persion_1_id = pairs[0] - a nx1 array
                # persion_2_id = pairs[1] - a nx1 array

                # Disaply the frames and read is user presses q/exit
                user_exit = display_obj.update(
                    boxed_current_frame, motion_frame, background_frame,act_frame_diff)

                # Choosing next frame
                prev_frame = current_frame
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

# cap = cv2.VideoCapture('http://service:Tata!123@192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779') #service:TATA!@123;service:Pass!234; 48.51           ;rtsp:/service:TATA!@123@192.168.48.51
# rtsp://192.168.48.51//rtsp_tunnel , rtsp:/service:TATA!@123@192.168.48.51
# print("Reading first frame...") #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=37660
# ret, image = cap.read() #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779

# Note: VideoCaptureAsync implemented here has same format as VideoCapture....just specify the link of ip cam as:
# cap = VideoCaptureAsync(src="videofile_name / Ip camera link")
cap = VideoCaptureAsync(src='../PNNLParkingLot2.avi')
# cap = VideoCaptureAsync(src=0)
# This is responsible for starting up the thread and frame capturing process
cap.start()
while True:
    detectMotion(cap)

# cv2.destroyAllWindows()

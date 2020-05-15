import numpy as np
import argparse
import cv2
import imutils
import sys
from scipy.spatial import distance
import datetime as dt
# VideoCaptureAsync implements separate thread for reading stream from camera
from visionObjects.videocaptureasync import VideoCaptureAsync
from visionObjects.frameDisplay import FrameDisplay
from visionObjects.distanceCalc import d_Calc
from visionObjects.backgroundDetection import backgroundCalc
from visionObjects.streamError import display_stream_error

# The below function is responsible for implementing the Detecting the motion.
timeDuration = dt.timedelta(seconds=40)
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
        if user_exit==True:
            cap.stop()
            display_obj.stop()
            sys.exit(0)

    else:
        fid = 1
        frame1 = cv2.resize(frame1, (640, 480))
        # Set first frame as default background
        mean_background_frame = frame1

        print("First frame Read")

        while True:
            # Read second and subsequent frames
            ret, frame2 = cap.read()
            if not ret or frame2 is None:
                print("[INFO] Cam IP Stream unavailable...")
                user_exit = display_obj.display_error()

            else:
                # print("fid - ",fid)
                motion_status = False
                # Resizing the frame
                frame1 = cv2.resize(frame1, (640, 480))
                frame2 = cv2.resize(frame2, (640, 480))
                # Applying appropiate filters
                frame = cv2.absdiff(frame1, frame2)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                threst_delta = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)[1]
                dilated = cv2.dilate(threst_delta, None, iterations=1)
                contours, _ = cv2.findContours(dilated,
                                               cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                #print(f"Number of contours found in {fid} frame = { len(contours) }")

                d_obj = d_Calc(frame1, threshold_dist, motion_status, contours)
                motion_status = d_obj.CalcDist(
                    frame1, threshold_dist, motion_status, contours)


                b_obj = backgroundCalc(
                    background_frames, mean_background_frame, frame_rate, desired_time_frame)
                # Changing background dynamically
                if motion_status:
                    mean_background_frame = b_obj.updateBackground(
                        background_frames, mean_background_frame, frame_rate, desired_time_frame)

                # No motion detected in frame1, so add to dictionary of background frame
                if not motion_status:
                    background_frames[fid] = frame1
                    # If no motion is detected for a long time
                    if len(background_frames) > 2 * frame_rate * desired_time_frame:
                        mean_background_frame = b_obj.updateBackground(
                            background_frames, mean_background_frame, frame_rate, desired_time_frame)

                # Displaying the frames
                user_exit = display_obj.update(frame1,threst_delta,mean_background_frame)
                # Choosing next frame
                frame1 = frame2
                fid += 1

            if user_exit==True:
                cap.stop()
                display_obj.stop()
                sys.exit(0)
                # break

        cap.stop()
        display_obj.stop()
        sys.exit(0)

# Intializing and starting the UI thread object
display_obj = FrameDisplay()
display_obj.start()
# cap = cv2.VideoCapture('http://service:Tata!123@192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779') #service:TATA!@123;service:Pass!234; 48.51           ;rtsp:/service:TATA!@123@192.168.48.51
# rtsp://192.168.48.51//rtsp_tunnel , rtsp:/service:TATA!@123@192.168.48.51
# print("Reading first frame...") #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=37660
# ret, image = cap.read() #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779

# Note: VideoCaptureAsync implemented here has same format as VideoCapture....just specify the link of ip cam as:
# cap = VideoCaptureAsync(src="videofile_name / Ip camera link")
# cap = VideoCaptureAsync(src='../PNNLParkingLot2.avi')
cap = VideoCaptureAsync(src=0)
# This is responsible for starting up the thread and frame capturing process
cap.start()
while True:
    detectMotion(cap)

# cv2.destroyAllWindows()

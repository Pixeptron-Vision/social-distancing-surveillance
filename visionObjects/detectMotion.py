import numpy as np
import argparse
import cv2
import datetime as dt
import imutils
import sys
from scipy.spatial import distance
# VideoCaptureAsync implements separate thread for reading stream from camera
from visionObjects.videocaptureasync import VideoCaptureAsync
from visionObjects.distanceCalc import d_Calc
from visionObjects.backgroundDetection import backgroundCalc
from visionObjects.streamError import display_stream_error


class detectMotionClass:

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

    def __init__(self, cap):
        self.cap = cap

    def detectMotion(self, cap, threshold_dist=75, frame_rate=15, desired_time_frame=int(timeDuration.seconds),  background_frames={}, motion_status=False, mean_background_frame=None
                     ):

        ret, frame1 = cap.read()
        fid = 1
        frame1 = cv2.resize(frame1, (640, 480))
        #global mean_background_frame
        mean_background_frame = frame1
        print("First frame Read")
        if not ret or frame1 is None:
            print("[INFO] Stream unavailable..!")
            cap.stop()
            # Return Flase to shows that the stream has breaked in between ot video file has reached end.
            return False

        while cap.isOpened():
            # Read second and subsequent frames
            ret, frame2 = cap.read()
            if not ret or frame2 is None:
                print("[INFO] Cam IP Stream unavailable...")
                cap.stop()
                return False
            else:
                motion_status = False
                # Resizing the frame
                frame1 = cv2.resize(frame1, (640, 480))
                frame2 = cv2.resize(frame2, (640, 480))
                # Applying appropiate filters
                frame = cv2.absdiff(frame1, frame2)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                threst_delta = cv2.threshold(
                    blur, 10, 255, cv2.THRESH_BINARY)[1]
                dilated = cv2.dilate(threst_delta, None, iterations=1)
                contours, _ = cv2.findContours(dilated,
                                               cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                #print(f"Number of contours found in {fid} frame = { len(contours) }")

                d_obj = d_Calc(frame1, threshold_dist, motion_status, contours)
                motion_status = d_obj.CalcDist(
                    frame1, threshold_dist, motion_status, contours)

                b_obj = backgroundCalc(
                    background_frames, mean_background_frame, frame_rate, desired_time_frame)
    #           Changing background dynamically
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
                cv2.imshow("Frame", frame1)
                cv2.imshow("Motion", threst_delta)
                # Displaying median background frame
                cv2.imshow("Background", mean_background_frame)
                # Choosing next frame
                frame1 = frame2
                fid += 1
                #ret, frame2 = video.read()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.stop()
                cv2.destroyAllWindows()
                sys.exit(0)
                break

        cap.stop()
        cv2.destroyAllWindows()
        # Returns True to display succesfull end of function and prevents returning garbage value
        return True

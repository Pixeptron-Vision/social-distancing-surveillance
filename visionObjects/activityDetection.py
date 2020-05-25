import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage import data
import matplotlib.pyplot as plt
from skimage.util import invert


def activity_filter(current_frame, background_frame, static_motion_frame):

    # Resizing the frames
    background_frame = cv2.resize(background_frame, (640, 480))
    static_motion_frame = cv2.resize(static_motion_frame, (640, 480))
    #background_frame = cv2.cvtColor(background_frame, cv2.COLOR_BGR2GRAY)
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    background_frame_blur = cv2.GaussianBlur(background_frame, (5, 5), 0)
    current_frame_blur = cv2.GaussianBlur(current_frame, (5, 5), 0)
    # Applying appropiate filters
    frame_diff = cv2.absdiff(background_frame_blur, current_frame_blur)
    # Static motion frame also taken into account for difference
    frame_diff = cv2.absdiff(frame_diff, static_motion_frame)
    # gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(frame_diff, (5, 5), 0)
    thresh_delta = cv2.threshold(
        frame_diff, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    activity = thresh_delta.copy()

    #kernel = np.ones((5,5),np.uint8)
    #erosion = cv2.erode(threst_delta,kernel,iterations = 1)
    dilated = cv2.dilate(thresh_delta, None, iterations=1)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate centers of each contours
    return (contours, calc_centers(contours, current_frame), dilated, frame_diff)


def calc_centers(contours, current_frame):
    centers = []
    boxed_current_frame = current_frame.copy()
    totalContourArea = 0
    thresh_activity = 0.5
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        totalContourArea += w * h
        # filtering out which contours to ignore
        if cv2.contourArea(cnt) < 500:
            continue
        cv2.rectangle(boxed_current_frame, (x-1, y-1),
                      (x+w-1-1, y+h-1-1), (255, 0, 0), 3)
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        centers.append([cx, cy])
    # TO ignore results due to camera Vibrations
    if totalContourArea > (current_frame.shape[0]*current_frame.shape[1])*thresh_activity:
        centers = []
        boxed_current_frame = current_frame
    return centers, boxed_current_frame

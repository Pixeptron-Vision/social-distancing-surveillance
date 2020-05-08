# -*- coding: utf-8 -*-
"""
Created on Wed May  6 15:59:50 2020

@author: Lakhan
"""

import numpy as np
import argparse
import cv2
import imutils

#Detects Motion from video by dynamically changing background
def detectMotion(cap , med_frames , desired_time_limit , desired_thresh , frame_rate):
    
#    Reading first frame
    print("Reading first frame...")
    ret, image = cap.read()
    
#    If no frames available then return
    print("First frame Read")
    if  not ret:
        print("[INFO] Stream unavailable..!")
        cap.release()
        return 
    
#    Taking first first frame as background 
    if ret:
        background_frame = image

#   Loop through video
    while(cap.isOpened()):

        ret, frame = cap.read()
        
        frame = cv2.resize(frame, (640, 480))
        cframe = frame.copy()
        background_frame = cv2.resize(background_frame, (640, 480))
        
#    Applying appropiate filters
        dframe = cv2.absdiff(frame, background_frame)
        
        gray = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
        
        blur = cv2.GaussianBlur(gray, (21, 21), 0)
        
        thresh_delta = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)[1]
        
        dilated = cv2.dilate(thresh_delta, None, iterations=2)
        cnts = cv2.findContours(dilated,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
#        Finding contours
        for cnt in cnts:
#            Contour below a certain value are ignored
            if cv2.contourArea(cnt) < 300:
                continue
#            Drawing rectangular box around contours
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x-1, y-1), (x+w, y+h), (255, 255, 255), 1)
            cv2.imshow("Motion" , frame)
                       
#        Changing background dynamically
#        Appends the first (desired_time_limit * frame_rate) frames
        if len(med_frames) <= (desired_time_limit * frame_rate):
            med_frames.append(cframe)
        else:
#           \Appends 1 new frame and 1 removes old frame 
            med_frames.pop(0)
            med_frames.append(cframe)
            
#            Difference between first and last frame of med_frame(list)
            background_diff = cv2.absdiff(med_frames[0] , med_frames[(desired_time_limit * frame_rate) - 1 ])
            
#            Grayscaling
            background_diff = cv2.cvtColor(background_diff , cv2.COLOR_BGR2GRAY)
            
#            Summation of all the element of background_diff
            m = np.sum(background_diff)
#            cv2.imshow("BackGround Difference" , background_diff)
#            cv2.waitKey(0)
            
#            Changing background_frame 
            if m < desired_thresh:
                background_frame = cframe
#                cv2.imshow('BackGround_frame' , cv2.resize(background_frame , (640 , 480)))
#                cv2.waitKey(0)
                
#    break loop if enter is pressed
        if cv2.waitKey(1) == 13:
            break
#
#
    cap.release()
    cv2.destroyAllWindows()
    


med_frames = []
desired_time_limit = 5
frame_rate = 25
desired_thresh = 700000
cap = cv2.VideoCapture('rtsp://service:Tata!123@192.168.51.5/1')
if cap.isOpened():
	# Function call to detect motion
        detectMotion(cap , med_frames , desired_time_limit , desired_thresh , frame_rate)    

cv2.destroyAllWindows()

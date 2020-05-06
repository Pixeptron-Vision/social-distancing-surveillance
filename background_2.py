

import numpy as np
import argparse
import cv2 
import imutils 


cap = cv2.VideoCapture('PNNLParkingLot2.avi')

# med_frames = []
# count = 0
# desired_time_limit = 5
# frame_rate = 25
# desired_thresh = 0.75

#med_frames will contain previous 10 frames of the current frames
med_frames = []
count = 0
cap = cv2.VideoCapture('PNNL_Parking_LOT(1).avi')
ret  , image = cap.read()

#unavailable stream
if ~ret:
    print("Stream Unavailable")

#taking first frame as intial background frame  
if ret:
    background_frame = image
    background_frame = cv2.cvtColor(background_frame , cv2.COLOR_BGR2GRAY)
    background_frame = cv2.GaussianBlur(background_frame , (21 , 21) , 0)

while(cap.isOpened()):
    ret, frame = cap.read()
    
#    grayscaling the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#   Gaussian Blur to conada activate reduce noise.
    gray = cv2.GaussianBlur(gray , (21 , 21) , 0)
    
    cgray = gray.copy()
    gray = gray.astype(dtype = np.float32)
    
    background_frame = background_frame.astype(dtype = np.float32)
    
#   taking difference between frame and background frame
    dframe = cv2.absdiff(gray , background_frame)
    dframe = dframe.astype(dtype=np.uint8)
    
    thresh = cv2.threshold(dframe, 10, 255,cv2.THRESH_BINARY)[1]
    
#    dilation and erosion
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    
#    finding contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
# loop over the contours
    for c in cnts:
# if the contour is too small, ignore it
        if cv2.contourArea(c) < 500:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
#finding median background frame using previous 10 frames
    if count<=10:
        med_frames.append(cgray)
        count+=1
    else:
        background_frame = np.median(med_frames , axis = 0)
        med_frames.pop(0)
        med_frames.append(cgray)


#     if len(med_frames) <= (desired_time_limit * frame_rate):
#         med_frames.append(cgray)
#     else:
#         med_frames.pop(0)
#         med_frames.append(cgray)
#         s = ssim(med_frames[0] , med_frames[-1])
#         if s >= desired_thresh:
#             background_frame = np.median(med_frames , axis = 0)
#             cv2.imshow('BackGround_frame' , cv2.resize(background_frame , (640 , 480)))
        
#    displaying the result
    cv2.imshow('frame',cv2.resize(frame , (640 , 480)))
    
#    break loop if enter is pressed
    if cv2.waitKey(1) == 13:
        break


cap.release()
cv2.destroyAllWindows()
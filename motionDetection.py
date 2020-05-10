import numpy as np
import argparse
import cv2
import imutils
import sys
from scipy.spatial import distance
from videocaptureasync import VideoCaptureAsync  #VideoCaptureAsync implements separate thread for reading stream from camera

# The below function is responsible for implementing the Detecting the motion.
def detectMotion(cap):

    print("Reading first frame...")
    ret, frame1 = cap.read()
    fid=1
    print("First frame Read")
    if  not ret or frame1 is None:
        print("[INFO] Stream unavailable..!")
        cap.stop()
        return False        #Return Flase to shows that the stream has breaked in between ot video file has reached end.

    while cap.isOpened():
        # second and subsequent frames
        ret, frame2 = cap.read()
        if  not ret or frame2 is None:
            print("[INFO] Cam IP Stream unavailable...")
            cap.stop()
            return False
        else :
            # Resizing the frame
            frame1 = cv2.resize(frame1, (640, 480))
            frame2 = cv2.resize(frame2, (640, 480))
            # Applying appropiate filters
            frame = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            blur = cv2.GaussianBlur(gray, (17, 17), 0)
            threst_delta = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)[1]
            dilated = cv2.dilate(threst_delta, None, iterations=3)
            contours, _ = cv2.findContours(dilated,
                                           cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            print(f"Number of contours found in {fid} frame = { len(contours) }")

            # Contours represent any motion occured between consequetive frames
            center = []  # Will contain centres of all contours
            print(" Finding center of contours")
            for cnt in contours:
                # filtering out which contours to ignore
                if cv2.contourArea(cnt) < 700:
                    continue
                # Drawing a rectangular box around the bounding points of contour
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(frame1, (x-1, y-1), (x+w-1-1, y+h-1-1), (255, 0, 0), 3)

                M = cv2.moments(cnt)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                center.append([cx, cy])
               # cv2.putText(frame1, "Status: {}".format("Motion Detected"),
                #            (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            #cv2.drawContours(frame1, countours, -1, (255, 0, 0), 3)
            # cv2.imshow('Stream',frame1)
            N = len(center)
            if N>1:

                # Find distance between all pairs
                D = distance.pdist(center)
                D = distance.squareform(D)
                # D
                threshold_dist = 75

                # ignore the upper triangle as the matrix will be symmetric so yo avoid repetation of pairs
                upper_tri = np.triu_indices(N, 0)
                D[upper_tri] = threshold_dist+100
                pairs = np.where(D < threshold_dist)

                person_1_id = pairs[0]
                person_2_id = pairs[1]
                print(len(pairs))
                # print(len(X))
                for i in range(len(person_1_id)):
                    cv2.circle(frame1, (center[person_1_id[i]][0],
                                        center[person_1_id[i]][1]), 10, (0, 0, 255), -1)
                    cv2.circle(frame1, (center[person_2_id[i]][0],
                                        center[person_2_id[i]][1]), 10, (0, 0, 255), -1)
                    # Displaying the frames
            cv2.imshow("Stream", frame1)
            cv2.imshow("Motion", threst_delta)
            # Choosing next frame
            frame1 = frame2
            fid += 1
            #ret, frame2 = video.read()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.stop()
            cv2.destroyAllWindows()
            sys.exit(0)
            break
    #cv2.waitKey(0)
    #cap.release()
    #out.release()
    cap.stop()
    cv2.destroyAllWindows()
    return True         #Returns True to display succesfull end of function and prevents returning garbage value




# Function for error display if stream is unavailable at start or camera port is inaccessible.
def display_stream_error():
    # cv2.destroyWindow('Camera Stream')
    cv2.destroyWindow('Motion')      # Destroys the rdundant gui window
    error_img = cv2.imread(r'stream_error.jpg')
    error_img = cv2.resize(error_img, (500,500), interpolation=cv2.INTER_AREA)
    print('Camera disconnected')
    #cap.release()
    cv2.imshow('Stream',error_img)
    cv2.waitKey(1000)                 # A 3 second refresh/halt to recheck connections




while True:
    #cap = cv2.VideoCapture('http://service:Tata!123@192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779') #service:TATA!@123;service:Pass!234; 48.51           ;rtsp:/service:TATA!@123@192.168.48.51
    # rtsp://192.168.48.51//rtsp_tunnel , rtsp:/service:TATA!@123@192.168.48.51
    # print("Reading first frame...") #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=37660
    # ret, image = cap.read() #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779


    #Note: VideoCaptureAsync implemented here has same format as VideoCapture....just specify the link of ip cam as:
    # cap = VideoCaptureAsync(src="videofile_name / Ip camera link")
    # cap = VideoCaptureAsync(src='PNNLParkingLot2.avi')
    cap = VideoCaptureAsync(src=0)
    cap.start()             # This is responsible for starting up the thread and frame capturing process
    if cap.isOpened():
        print('Camera is connected')
        response = detectMotion(cap)
        if response == False:
            display_stream_error() #Call the function to display the error message
            continue
    else:                                # If system is unable to open/access the camera port.
        display_stream_error()
        continue

# cap = cv2.VideoCapture(0)
cv2.destroyAllWindows()
# detectMotion(cap)

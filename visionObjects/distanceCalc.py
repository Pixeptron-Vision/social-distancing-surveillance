import cv2
from scipy.spatial import distance
import numpy as np


class d_Calc:
    def __init__(self , frame1 , threshold_dist , motion_status , contours):
        self.frame1 = frame1
        self.threshold_dist = threshold_dist 
        self.motion_status = motion_status
        self.contours = contours
    
    def CalcDist(self , frame1 , threshold_dist , motion_status , contours):
        center = []
        for cnt in contours:
        # filtering out which contours to ignore
            if cv2.contourArea(cnt) < 500:
                continue
            motion_status = True
#            cframe1 = frame1.copy()
        # Drawing a rectangular box around the bounding points of contour
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame1, (x-1, y-1), (x+w-1-1, y+h-1-1), (255, 0, 0), 3)
        
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            center.append([cx, cy])
        
#        cv2.putText(frame1, "Status: {}".format("Motion Detected"),
#                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #cv2.drawContours(frame1, countours, -1, (255, 0, 0), 3)
        print(center)
        N = len(center)
        if N>1:
        
        # Find distance between all pairs
            D = distance.pdist(center)
            D = distance.squareform(D)
        # D
        

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
            cv2.imshow("Frame", frame1)
            return motion_status
        
import cv2
from scipy.spatial import distance
import numpy as np


def calculate_dist(boxed_current_frame, center,threshold_dist):
    N = len(center)
    pairs=None
    if N > 1:
        # Find distance between all pairs
        D = distance.pdist(center)
        D = distance.squareform(D)

        # ignore/mask the upper triangle with 0 as the matrix will be symmetric so yo avoid repetation of pairs
        upper_tri = np.triu_indices(N, 0)
        #Add 1000 to increase value of upper triangle such thay it does not comes less than threshold
        D[upper_tri] = threshold_dist+1000
        pairs = np.where(D < threshold_dist)

        person_1_id = pairs[0]
        person_2_id = pairs[1]
        # print(len(pairs))
        for i in range(len(person_1_id)):
            cv2.circle(boxed_current_frame, (center[person_1_id[i]][0],
                                    center[person_1_id[i]][1]), 2, (0, 0, 255), -1)
            cv2.circle(boxed_current_frame, (center[person_2_id[i]][0],
                                    center[person_2_id[i]][1]), 2, (0, 0, 255), -1)
        # Displaying the frames
        # cv2.imshow("Frame", frame1)
    return pairs

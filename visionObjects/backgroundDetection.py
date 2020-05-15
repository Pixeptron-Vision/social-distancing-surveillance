import cv2
import numpy as np


class backgroundCalc:
    def __init__(self, background_frames=None, mean_background_frame=None, frame_rate=None, desired_time_frame=None):
        self.background_frames = background_frames
        self.mean_background_frame = mean_background_frame
        self.frame_rate = frame_rate
        self.desired_time_frame = desired_time_frame

    def updateBackground(self, background_frames, mean_background_frame, frame_rate, desired_time_frame):
        # if no of frames in background_frames > threshold no of frames to update
        if len(background_frames) > frame_rate * desired_time_frame:
            # Taking the mean of background frames using the frame id
            background_id = []
            for i in sorted(background_frames.keys()):
                background_id.append(i)
            np_background_id = np.array(background_id)
            # mean frame id of background
            mean_id = int(np.mean(np_background_id))
            np_background_id = np_background_id[np_background_id >= mean_id]
            # mean background frame itself
            mean_background_frame = background_frames[np_background_id[0]]
            # making the dictionary empty
            background_frames.clear()
            return mean_background_frame
        return mean_background_frame

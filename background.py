import cv2
import numpy as np
import datetime as dt


video = cv2.VideoCapture('cctv.mp4')

# Initialising the the threshold time for latest common static background frame
#timeDuration = dt.timedelta(seconds=20)
#desired_time_frame = int(timeDuration.seconds)
desired_time_frame = 20
frame_rate = 25

# For background frame, intialising a background_frames dictionary
background_frames = {}


# first frame
motion_status = False
if video.isOpened:
    ret, frame1 = video.read()
    fid = 1
    # Selecting first frame as background
    frame1 = cv2.resize(frame1, (640, 480))
    mean_background_frame = frame1

while video.isOpened():
    # second and subsequent frames
    ret, frame2 = video.read()

    motion_status = False

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

    # Contours represent any motion occured between consequetive frames
    for cnt in contours:
        # filtering out which contours to ignore
        if cv2.contourArea(cnt) < 500:
            continue
        motion_status = True
        # Drawing a rectangular box around the bounding points of contour
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame1, (x-1, y-1), (x+w-1-1, y+h-1-1), (255, 0, 0), 3)
        cv2.putText(frame1, "Status: {}".format("Motion Detected"),
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #cv2.drawContours(frame1, countours, -1, (255, 0, 0), 3)

    # Updating background frame only during motion
    if motion_status:
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

    # No motion detected in frame1, so add to dictionary of background frame
    if not motion_status:
        background_frames[fid] = frame1

    # Displaying the frames
    cv2.imshow("Frame", frame1)
    cv2.imshow("Motion", threst_delta)
    # Displaying median background frame
    cv2.imshow("Background", mean_background_frame)

    # Choosing next frame
    frame1 = frame2
    fid += 1
    #ret, frame2 = video.read()

    # Press ENTER to break the loop
    key = cv2.waitKey(1)
    if(key == 13):
        break

video.release()
cv2.destroyAllWindows()

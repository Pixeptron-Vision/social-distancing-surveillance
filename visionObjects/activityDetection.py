import cv2

def activity_filter(current_frame, background_frame):

    # Resizing the frames
    background_frame = cv2.resize(background_frame, (640, 480))
    # Applying appropiate filters
    frame_diff = cv2.absdiff(current_frame, background_frame)
    gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    threst_delta = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)[1]
    dilated = cv2.dilate(threst_delta, None, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate centers of each contours
    return (contours , calc_centers(contours,current_frame))

def calc_centers(contours,current_frame):
    centers = []
    boxed_current_frame = current_frame.copy()
    for cnt in contours:
        # filtering out which contours to ignore
        if cv2.contourArea(cnt) < 500:
            continue
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(boxed_current_frame, (x-1, y-1),(x+w-1-1, y+h-1-1), (255, 0, 0), 3)
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        centers.append([cx, cy])

    return centers , boxed_current_frame

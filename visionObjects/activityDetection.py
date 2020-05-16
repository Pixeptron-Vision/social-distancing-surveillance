import cv2


class activity:
    background_frame = None
    current_frame = None
    centers = []
    contours = None

    def activity_filter(self, current_frame, background_frame):
        # Saving the frames
        self.current_frame = current_frame
        self.background_frame = background_frame
        # Vacating the centers and contours
        self.contours = None
        self.centers = []

        # Resizing the frames
        current_frame = cv2.resize(current_frame, (640, 480))
        background_frame = cv2.resize(background_frame, (640, 480))
        # Applying appropiate filters
        frame_diff = cv2.absdiff(current_frame, background_frame)
        gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        threst_delta = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)[1]
        dilated = cv2.dilate(threst_delta, None, iterations=1)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Saving the contours
        self.contours = contours

        # Calculate centers of each contours
        self.calc_centers(contours)

    def calc_centers(self, contours):
        for cnt in contours:
            # filtering out which contours to ignore
            if cv2.contourArea(cnt) < 500:
                continue

            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            self.centers.append([cx, cy])

    def get_centers(self):
        return self.centers

    def get_contours(self):
        return self.contours

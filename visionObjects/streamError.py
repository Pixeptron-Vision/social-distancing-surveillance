import cv2


# Function for error display if stream is unavailable at start or camera port is inaccessible.
def display_stream_error():
    # cv2.destroyWindow('Camera Stream')
    # Destroys the rdundant gui window
    cv2.destroyWindow('Background')
    cv2.destroyWindow('Motion')
    error_img = cv2.imread(r'stream_error.jpg')
    error_img = cv2.resize(error_img, (640, 480), interpolation=cv2.INTER_AREA)
    print('Camera disconnected')
    # cap.release()
    cv2.imshow('Frame', error_img)
    # A 3 second refresh/halt to recheck connections
    cv2.waitKey(1000)

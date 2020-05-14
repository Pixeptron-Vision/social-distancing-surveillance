import cv2
# VideoCaptureAsync implements separate thread for reading stream from camera
from visionObjects.videocaptureasync import VideoCaptureAsync
from visionObjects.streamError import display_stream_error
from visionObjects.detectMotion import detectMotionClass

while True:
    # cap = cv2.VideoCapture('http://service:Tata!123@192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779') #service:TATA!@123;service:Pass!234; 48.51           ;rtsp:/service:TATA!@123@192.168.48.51
    # rtsp://192.168.48.51//rtsp_tunnel , rtsp:/service:TATA!@123@192.168.48.51
    # print("Reading first frame...") #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=37660
    # ret, image = cap.read() #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779
    # Note: VideoCaptureAsync implemented here has same format as VideoCapture....just specify the link of ip cam as:
    # cap = VideoCaptureAsync(src="videofile_name / Ip camera link")
    cap = VideoCaptureAsync(src='cctv(2).mp4')
    # cap = VideoCaptureAsync(src=0)
    # This is responsible for starting up the thread and frame capturing process
    cap.start()
    if cap.isOpened():
        print('Camera is connected')
        d_motion = detectMotionClass(cap)
        response = d_motion.detectMotion(cap)
        if response == False:
            display_stream_error()  # Call the function to display the error message
            continue
    # If system is unable to open/access the camera port.
    else:
        display_stream_error()

cv2.destroyAllWindows()

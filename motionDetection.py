import numpy as np
import argparse
import cv2 
import imutils 																										
#cap = cv2.VideoCapture('http://service:Tata!123@192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779') #service:TATA!@123;service:Pass!234; 48.51 ;rtsp:/service:TATA!@123@192.168.48.51
cap = cv2.VideoCapture("PNNLParkingLot2.avi") # rtsp://192.168.48.51//rtsp_tunnel , rtsp:/service:TATA!@123@192.168.48.51
print("Reading first frame...") #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=37660
ret, image = cap.read() #http://192.168.51.77/video.mp4?line=1&inst=1&rec=0&rnd=60779
image = cv2.resize(image,(640,480))
cv2.waitKey(1)
print("First frame Read")
if ~ret:
	print("[INFO] Stream unavailable..!") 
if ret:
	frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)
	# Display median frame	
	# Store selected frames in an array
	frames = []
	for fid in frameIds:
		cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
		ret, frame = cap.read()
		frame = cv2.resize(frame,(640,480))
		frames.append(frame)
		# Calculate the median along the time axis
		medianFrame = np.median(frames, axis=0).astype(dtype=np.float32) 
		grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
		grayMedianFrame = cv2.GaussianBlur(grayMedianFrame, (21, 21), 0)
#out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
while(True):	
	#print "In loop"
	ret, frame = cap.read()
	if ~ret:
		print("[INFO] Cam IP Stream unavailable...") 

	if ret:

		frame = cv2.resize(frame,(640,480))
		cframe = np.copy(frame)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)		
		gray = cv2.GaussianBlur(frame, (21, 21), 0)
		gray = gray.astype(dtype = np.float32)

		# saliency = cv2.saliency.StaticSaliencyFineGrained_create()
		# (success, saliencyMap) = saliency.computeSaliency(frame)#gdialc[:,:,2]
		# saliencyMap = (saliencyMap * 255).astype("uint8")
		# threshMap = cv2.threshold(saliencyMap, 0, 255,cv2.THRESH_OTSU)[1] #cv2.ADAPTIVE_THRESH_MEAN_C | 	

		#cv2.accumulateWeighted(gray, avg, 0.5)
		#frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

		dframe = cv2.absdiff(gray, grayMedianFrame)
		dframe = dframe.astype(dtype=np.uint8)
		thresh = cv2.threshold(dframe, 10, 255,cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < 5000:
				continue
	 
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
	    # Display image
		#cv2.imshow('Saliency',cv2.resize(saliencyMap,(640,480)))
		#cv2.imshow('Motion',dframe.astype(dtype=np.uint8))		
		cv2.imshow('Stream',frame)
		cv2.imshow('Motion',cv2.resize(dframe.astype(dtype=np.uint8),(640,480)))						
		# Randomly select 25 frames
		#cv2.imshow('Medianframe', medianFrame)
   
		"""


		(h, w,d) = image.shape#[:2]
		print "h,w,depth",h,w,d
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)		
		#gray=strip.copy()
		retval, threshold = cv2.threshold(gray, int((np.amax(gray)-np.amin(gray))*0.85), 255, cv2.THRESH_BINARY)
		# show the output image		
		cv2.imshow('Threshold',cv2.resize(threshold,(640,480))) #image
		cv2.imshow('Input Frame',cv2.resize(image,(640,480))) #image	
		#out.write(image)	
		"""
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#cv2.waitKey(0)
cap.release()
#out.release()
cv2.destroyAllWindows()



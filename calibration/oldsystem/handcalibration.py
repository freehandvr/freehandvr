from ast import literal_eval
from imutils.video import VideoStream
import cv2
import imutils
import numpy as np
import sys
import re
import tkinter

## need to run this twice, one red and one blue

## specify red or blue

if len(sys.argv) != 3:
	print 'Wrong options'
	exit(1)

if "hand" in sys.argv[1]:
	filename = 'hand.txt'

number = int(re.search(r'\d+', sys.argv[2]).group())

def nothing(x):
    pass
cv2.namedWindow('Hand Calibration')

# Starting with 100's to prevent error while masking
lower = (100, 100, 100)
higher = (255, 255, 255)

# Creating track bar

higher = (255, 255, 255)
text = "Default Options: Lower(30,30,80), Upper(180,180,255)"
cv2.createTrackbar('LowH', 'Hand Calibration',0,255,nothing)
cv2.createTrackbar('LowS', 'Hand Calibration',0,255,nothing)
cv2.createTrackbar('LowV', 'Hand Calibration',0,255,nothing)
cv2.createTrackbar('HighH', 'Hand Calibration',0,255,nothing)
cv2.createTrackbar('HighS', 'Hand Calibration',0,255,nothing)
cv2.createTrackbar('HighV', 'Hand Calibration',0,255,nothing)

while True:

	#read the image from the camera
	videoSrc = VideoStream(src=number).start()    

	#You will need this later
	frame = videoSrc.read()
		
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	
	print text
	
	# get info from track bar and appy to result
	lowh = cv2.getTrackbarPos('LowH', 'Hand Calibration')
	lows = cv2.getTrackbarPos('LowS', 'Hand Calibration')
	lowv = cv2.getTrackbarPos('LowV', 'Hand Calibration')
	highh = cv2.getTrackbarPos('HighH', 'Hand Calibration')
	highs = cv2.getTrackbarPos('HighS', 'Hand Calibration')
	highv = cv2.getTrackbarPos('HighV', 'Hand Calibration')

	lower = (lowh, lows, lowv)
	higher = (highh,highs,highv)
        

	mask = cv2.inRange(hsv, lower, higher)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 12:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 0, 255), 2)
			cv2.circle(frame, center, 5, (255, 255, 255), -1)
	# Quit the program when Q is pressed
	cv2.imshow('Main Output', frame)
	cv2.imshow('Calibrated Hand Detection', mask)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

text_file = open(filename, "w")
## first line is low, second line is high
text_file.write("("+str(lowh)+","+str(lows)+","+str(lowv)+")\n")
text_file.write("("+str(highh)+","+str(highs)+","+str(highv)+")")
text_file.close()
cv2.destroyAllWindows()
print number
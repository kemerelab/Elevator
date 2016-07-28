from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from scipy.misc import imresize


import socket
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


UDP_IP = "127.0.0.1"
UDP_PORT = 5005



sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP



def percentdif(imageA, imageB):
	s = cv2.absdiff(imageA.astype("float"), imageB.astype("float"))
	s  = (s*100)/255
	s = np.sum(s)/(float(imageA.shape[0] * imageA.shape[1]))
	return s

def takepic():
	rawCap = PiRGBArray(camera)
	camera.capture(rawCap, format="bgr")
	image2 = rawCap.array
	gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
	return gray2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()

camera.resolution = (320, 240)
camera.framerate = 30

#rawCapture = PiRGBArray(camera)

# Wait for the automatic gain control to settle
time.sleep(3)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

rawCapture = PiRGBArray(camera)
#camera.resolution = (640, 480)
#raw = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(0.1)
 
# grab an image from the camera
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#cv2.imshow("gray", gray)

# we need this !?
#rawCapture = PiRGBArray(camera)
gray = None

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text

	image = frame.array
	
	if gray is None:
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		#cv2.imshow("gray", gray)
	 
	# show the frame
	#small = imresize(image, 0.5)
	#plt.imshow(image)
	#plt.show(False)
	#plt.draw()
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 	
	#camera.capture(rawCap, format="bgr")
	image2 = rawCapture.array
	gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#cv2.imshow("gray2", gray2)
	val = percentdif(gray, gray2)
	val = str(val)
	sock.sendto(val, (UDP_IP, UDP_PORT))
	#print('{:2.2f}'.format(percentdif(gray, gray2)))
	#time.sleep(1)


	
	
	
		
		


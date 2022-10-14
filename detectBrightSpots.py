from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import math

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image file")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY) [1]
#thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY) [1]
labels = measure.label(thresh, background=0)
mask = np.zeros(thresh.shape, dtype="uint8")
for label in np.unique(labels):
	print("Label: ", label)
	if label==0:
		continue
	labelMask = np.zeros(thresh.shape, dtype="uint8")
	labelMask[labels == label] = 255
	numPixels = cv2.countNonZero(labelMask)
	if numPixels > 2:
		mask = cv2.add(mask, labelMask)

cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = contours.sort_contours(cnts) [0]
f = open('/home/brynm/sf2022/starConnections/starCoords.txt', 'w')
x2 = y2 = 0
loops = 0
middleX = 2000
middleY = 1500
for (i, c) in enumerate(cnts):
	(x, y, w, h) = cv2.boundingRect(c)
	((cX, cY), radius) = cv2.minEnclosingCircle(c)
	print(x, y)
	hypo = str(math.hypot(math.fabs(x2-x), math.fabs(y2-y)))
	#f.write(str(math.hypot(math.fabs(x2-x), math.fabs(y2-y)))+"\n")
	cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
	x2 = x
	y2 = y
	if(x<=middleX):
		x=x-middleX
	elif(x>middleX):
		x=x-middleX
	if(y>middleY):
		y=middleY-y
	elif(y<=middleY):
		y=middleY-y
	cv2.putText(image, "("+str(x)+","+str(y)+")", (x2, y2-15), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2)
	#cv2.line(image, (x, y), (x2, y2), (0, 0, 255), 9)
	print("Loops: ", loops)
	loops = 1 + loops
	distance = math.hypot(math.fabs(2153-x), math.fabs(509-y))
	#distance = math.hypot(math.fabs(1771-x), math.fabs(2470-y))
	print("Distance: ", str(distance))
	f.write(str(x)+" , "+str(y)+"\n")
f.close()
path = '/home/brynm/sf2022/cStar/image.png'
cv2.imwrite('image.png', image)
#cv2.imshow("Image", image)
#cv2.waitKey(0)

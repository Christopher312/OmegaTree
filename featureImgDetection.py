import numpy as np
import cv2

W = 500.0
Y_CUTOFF1 = 420
Y_CUTOFF2 = 300
Y_CUTOFF3 = 150
X_CUTOFF1 = 115
X_CUTOFF2 = 250
X_CUTOFF3 = 375

def findNumDots(img):
	lower = np.array([0, 0, 0])
	upper = np.array([15, 15, 15])
	shapeMask = cv2.inRange(img, lower, upper)
	cv2.imshow("Mask", shapeMask)
	cv2.waitKey(0)

	# find the contours in the mask
	cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#for c in cnts:
		# draw the contour and show it
		#cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
		#cv2.imshow("Image", img)
		#cv2.waitKey(0)
	return len(cnts)

def determineList():
	l = []
	oriimg = cv2.imread("IMG_0160.JPG",cv2.IMREAD_COLOR)
	height, width, depth = oriimg.shape
	imgScale = W / width
	newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
	image = cv2.resize(oriimg,(int(newX),int(newY)))
	findNumDots(image)
	crop1 = image[X_CUTOFF1:X_CUTOFF2, Y_CUTOFF1:500]
	x = findNumDots(crop1)
	if(x==0):
		l.append(None)
	else:
		l.append(x-1)
	cv2.imshow("cropped", crop1)
	cv2.waitKey(0)
	crop2 = image[0:X_CUTOFF2, Y_CUTOFF2:Y_CUTOFF1]
	x = findNumDots(crop2)
	if(x==0):
		l.append(None)
	else:
		l.append(x-1)
	crop3 = image[X_CUTOFF2:500, Y_CUTOFF2:Y_CUTOFF1]
	x = findNumDots(crop3)
	if(x==0):
		l.append(None)
	else:
		l.append(x-1)
	crop4 = image[0:X_CUTOFF1, Y_CUTOFF3:Y_CUTOFF2]
	x = findNumDots(crop4)
	if(x==0):
		l.append(None)
	else:
		l.append(x-1)
	crop5 = image[X_CUTOFF1:X_CUTOFF2, Y_CUTOFF3:Y_CUTOFF2]
	x = findNumDots(crop5)
	if(x==0):
		l.append(None)
	else:
		l.append(x-1)
	crop6 = image[X_CUTOFF2:X_CUTOFF3, Y_CUTOFF3:Y_CUTOFF2]
	x = findNumDots(crop6)
	if(x==0):
		l.append(None)
	else:
		l.append(x-1)
	crop7 = image[X_CUTOFF2:500, Y_CUTOFF3:Y_CUTOFF2]
	x = findNumDots(crop7)
	if(x==0):
		l.append(None)
	else:
		l.append(x-1)
	return l

print(determineList())

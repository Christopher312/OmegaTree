import numpy as np
import argparse
import cv2

filename = "IMG_0160.JPG"
W = 500.
oriimg = cv2.imread(filename, cv2.IMREAD_COLOR)
height, width, depth = oriimg.shape
imgScale = W / width
newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
image = cv2.resize(oriimg,(int(newX),int(newY)))

output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=60, minRadius=5)

if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")

	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		if(r<80):
			print("radius: ", r)
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)


	cv2.imwrite("detect_circles_img.jpg", image)
	print("wrote image")
	cv2.imshow("output", np.hstack([image, output]))
	print("showing ootput")
	cv2.waitKey(0)
else:
	print("no circles detected")

def findNumCircles(img):
	lower = np.array([0, 0, 0])
	upper = np.array([15, 15, 15])
	shapeMask = cv2.inRange(image, lower, upper)

	# find the contours in the mask
	cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return cnts
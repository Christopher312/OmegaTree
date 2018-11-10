# import the necessary packages
import numpy as np
import argparse
import cv2
 
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required = True, help = "Path to the image")
#args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
filename = 'images/circleTest.jpg'
W = 1000.
oriimg = cv2.imread(filename,cv2.CV_LOAD_IMAGE_COLOR)
height, width, depth = oriimg.shape
imgScale = W/width
newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
image = cv2.resize(oriimg,(int(newX),int(newY)))

output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100) #, param1=128, minRadius=10, maxRadius=50)
 
# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
 
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
                print "radius: ", r
		#cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		#cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
                if (r<100):
		  cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		  cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 

	# show the output image
        
        cv2.imwrite("detect_circles_img.jpg", image)
	print "wrote image"
        cv2.imshow("output", np.hstack([image, output]))
	print "showing ooutput"
        cv2.waitKey(0)
else:
   print "no circles detected"


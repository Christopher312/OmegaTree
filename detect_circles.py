# import the necessary packages
import numpy as np
import argparse
import cv2
 
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required = True, help = "Path to the image")
#args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
#filename = 'images/circleTest.jpg'
#filename = 'newCircleTest.jpg'
filename = 'crop0final.jpg'
W = 1000.
oriimg = cv2.imread(filename,cv2.CV_LOAD_IMAGE_COLOR)
height, width, depth = oriimg.shape
imgScale = W/width
newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
image = cv2.resize(oriimg,(int(newX),int(newY)))


output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.5, 100)#, param2=1) #, param1=128, minRadius=10, maxRadius=50)
 
def max(x,y):
   if (x>y):
      return x
   else:
      return y

def sortFunction(r,x,y):
   return max(y-500, 0)**4+ r*r


def circle_helper(image):
   output = image.copy()
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   # detect circles in the image
   circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 1,  minRadius=0, maxRadius=20)
   # ensure at least some circles were found
   if circles is not None:
           # convert the (x, y) coordinates and radius of the circles to integers
           circles = np.round(circles[0, :]).astype("int")
           # loop over the (x, y) coordinates and radius of the circles
           for (x, y, r) in circles:
                   # draw the circle in the output image, then draw a rectangle
                   # corresponding to the center of the circle
                     cv2.putText(output, str(r)+","+str(x)+","+str(y), (x,y),cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0),2) #  Scalar(0,0,255,255), 2)
                     cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                     cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                     cv2.rectangle(output, (x - r, y - r), (x + r, y + r), (0, 128, 255), 4)
           # show the output image
           cv2.imwrite("detect_circles_img.jpg", image)
           print "wrote image"
           cv2.imshow("output", np.hstack([image, output]))
           print "showing ooutput"
           cv2.waitKey(0)
   else:
      print "no circles detected"




# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
 
	# loop over the (x, y) coordinates and radius of the circles
	radiusList = []
        for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
                print "radius: ", r, ", x: ", x,", y:", y
                
                radiusList.append(sortFunction(r,x,y))
		#cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		#cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        radiusList.sort()
        goodCircleList = []
 	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		  cv2.putText(output, str(r)+","+str(x)+","+str(y), (x,y),cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0),2) #  Scalar(0,0,255,255), 2)
                  cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		  cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                  cv2.rectangle(output, (x - r, y - r), (x + r, y + r), (0, 128, 255), 4)
                  
                  goodCircleList.append([r,x,y])

        counter=0

        """
        for (r,x,y) in goodCircleList:
            print "r: ", r, ", x: ", x,", y: ",y
            print "crop-dim: ","(",x-r,":",x+r,") (",y-r,":",y+r,")"
            crop1 = image[ y-r:y+r, x-r:x+r]
            cv2.imwrite("crop"+str(counter)+".jpg", crop1)
            counter = counter+1
            circle_helper(crop1)
             


	# show the output image
        """
        cv2.imwrite("detect_circles_img.jpg", image)
	print "wrote image"
        cv2.imshow("output", np.hstack([image, output]))
	print "showing ooutput"
        cv2.waitKey(0)
else:
   print "no circles detected"



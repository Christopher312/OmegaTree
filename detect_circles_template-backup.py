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
filename = 'newCircleTest7.jpg'
W = 1000.
oriimg = cv2.imread(filename,cv2.CV_LOAD_IMAGE_COLOR)
height, width, depth = oriimg.shape
imgScale = W/width
newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
image = cv2.resize(oriimg,(int(newX),int(newY)))
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 2, 150, maxRadius = 75)#,  maxRadius = 80)#, maxRadius = 80) #, param1=128, minRadius=10, maxRadius=50)
#
def max(x,y):
   if (x>y):
      return x
   else:
      return y

def sortFunction(r,x,y):
   return max(y-500, 0)**4+ r*r

def findLoc(image, template, threshold):
    img_rgb = image
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    return res

def circle_helper(oriimg):
    W = 220.
    height, width, depth = oriimg.shape
    imgScale = W/width
    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    image = cv2.resize(oriimg,(int(newX),int(newY)))
 
    output = image.copy()
 
    templateResult = []
    templates = ["mask0.png", "mask1.png", "mask2.png", "mask3.png", "mask4.png"]
    for i in range(len(templates)):
        loc = findLoc(image, templates[i], 0.5)
        templateResult.append(loc)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(loc)
        print "template ",i
        print "max_val", max_val


#ensure at least some circles were found
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
        print "circles master list: ", circles
        goodCircleList = []
        counter = 0
 	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
                if (sortFunction(r,x,y)<=radiusList[6]):
		  cv2.putText(output, str(r)+","+str(x)+","+str(y), (x,y),cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0),2) #  Scalar(0,0,255,255), 2)
                  cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		  cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                  cv2.rectangle(output, (x - r, y - r), (x + r, y + r), (0, 128, 255), 4)
                  
                  crop1 = image[ y-r+10:y+r-10, x-r+10:x+r-10]
                  cv2.imwrite("crop"+str(counter)+".jpg", crop1)
	          print "working on crop ",counter
                  numCircles = circle_helper(crop1)
                  cv2.putText(output, "numCircles:"+str(numCircles), (x,y+20),cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0),2) #  Scalar(0,0,255,255), 2)
                  counter = counter+1    
	# show the output image
        
        cv2.imwrite("detect_circles_img.jpg", image)
	print "wrote image"
        cv2.imshow("output", np.hstack([image, output]))
	print "showing ooutput"
        cv2.waitKey(0)
else:
   print "no circles detected"



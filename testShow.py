import cv2
import numpy as np

filename = 'images/IMG_MANY.JPG'
W = 1000.
oriimg = cv2.imread(filename,cv2.CV_LOAD_IMAGE_COLOR)
height, width, depth = oriimg.shape
imgScale = W/width
newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
newimg = cv2.resize(oriimg,(int(newX),int(newY)))


#img = cv2.imread('images/IMG_MANY.JPG')
#print(img)
cv2.imshow('Image', newimg)
cv2.waitKey(0)
cv2.imwrite("resizeimg.jpg", newimg)

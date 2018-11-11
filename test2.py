from pyzbar import pyzbar
import argparse
import numpy as np
import cv2

image =cv2.imread("image1.jpeg")

# thresholds image to white in back then invert it to black in white
#   try to just the BGR values of inRange to get the best result
thresholded = cv2.inRange(image,(0,0,0),(200,200,200))
inverted = 255-cv2.cvtColor(thresholded,cv2.COLOR_GRAY2BGR) # black-in-white
pyzbar.display(inverted);


decodedObjects = decode(Image.open('test2.png'))
obj = decodedObjects
for bar in obj:
  print(bar.data)

print (barcodes)


"""from PIL import Image
from pyzbar.pyzbar import decode
data = decode(Image.open('image1.jpeg'))
print(data)"""

from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import numpy

decodedObjects = decode(Image.open('image1_copy.jpeg'))
obj = decodedObjects
print len(obj)
for bar in obj:
  print(bar.data)

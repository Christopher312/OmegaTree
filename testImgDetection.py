import cv2
import numpy as np
from matplotlib import pyplot as plt

Y_CUTOFF1 = 400
Y_CUTOFF2 = 1000
X_CUTOFF1 = 1500
X_CUTOFF2 = 2000
X_CUTOFF3 = 1500
'''
img_rgb = cv2.imread('mario.png')
#img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('mario_coin.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)'''


def findLoc(imgName, template, threshold):
    img_rgb = cv2.imread(imgName)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return loc

def processImg(imgName):
    templates = ["mask0.png", "mask1.png", "mask2.png", "mask3.png", "mask4.png", "mask5.png", "mask6.png",
      "mask7.png"]
    branches = [None] * 7
    for i in range(len(templates)):
        loc = findLoc(imgName, templates[i], 0.5)
        for pt in zip(*loc[::-1]):
            x = pt[0]
            y = pt[1]
            if(y<Y_CUTOFF1):
                branches[0] = i
            elif(y<Y_CUTOFF2 and x < X_CUTOFF2):
                branches[1] = i
            elif(y<Y_CUTOFF2 and x >= X_CUTOFF2):
                branches[2] = i
            elif(y>=Y_CUTOFF2 and x < X_CUTOFF1):
                branches[3] = i
            elif(y>=Y_CUTOFF2 and x < X_CUTOFF2):
                branches[4] = i
            elif(y>=Y_CUTOFF2 and x < X_CUTOFF3):
                branches[5] = i
            elif(y>=Y_CUTOFF2 and x >= X_CUTOFF3):
                branches[6] = i
    return branches

print(processImg("maskTest.jpeg"))

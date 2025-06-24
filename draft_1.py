import numpy as np
import os
import cv2
img=cv2.imread('img1.jpg')
hsvi=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
grayi=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
grayi=cv2.medianBlur(grayi,1)
grayi=cv2.equalizeHist(grayi)
lred1=tuple(np.array([0,5,5]))
ured1=tuple(np.array([10,255,255]))
lred2=tuple(np.array([160,5,5]))
ured2=tuple(np.array([179,255,255]))
"""
lorange=np.array([15,5,5])
uorange=np.array([20,255,255])
"""
lgreen=tuple(np.array([25,5,5]))
ugreen=tuple(np.array([99,255,255]))
lblue=tuple(np.array([100,5,5]))
ublue=tuple(np.array([130,255,255]))
pswd=''
circles=cv2.HoughCircles(grayi,cv2.HOUGH_GRADIENT,dp=1,minDist=20,param1=30,param2=20,minRadius=5,maxRadius=35)
if circles is not None:
  circles=np.uint16(np.around(circles[0]))
  circles=sorted(circles,key=lambda c:(c[1],c[0]))
  rows=[]
  i=0
  for i in range(8):
    rows.append(circles[i*8:(i+1)*8:])
    if i%2==1:
      rows[i]=rows[i][::-1]
  for row in rows:
    for (x,y,r) in row:
      h, w = hsvi.shape[:2]
      x1, x2 = max(x-2, 0), min(x+3, w)
      y1, y2 = max(y-2, 0), min(y+3, h)
      roi = hsvi[y1:y2, x1:x2]
      pixel=tuple(np.mean(roi.reshape(-1, 3), axis=0).astype(int))
      if ((lred1<=pixel and pixel<=ured1) or (lred2<=pixel and pixel<=ured2)):
        pswd+='01'
      elif (lgreen<=pixel and pixel<=ugreen):
        pswd+='10'
      elif (lblue<=pixel and pixel<=ublue):
        pswd+='11'
      else:
        pswd+='00'
print("Password in binary: ",pswd)

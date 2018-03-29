#!/usr/bin/env python

from scipy.ndimage import convolve
import argparse
import video_search
import numpy as np
import scipy.signal as sp
import scipy.ndimage.filters as sp2
import cv2
import glob
from scipy.io import wavfile
from video_tools import *
import feature_extraction as ft    
import sys
import os
from video_features import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#parser = argparse.ArgumentParser(description="Video finding tool")
#parser.add_argument("query", help="video")
#parser.add_argument("-s", help="Timestamp for start of query in seconds", default=0.0)
#parser.add_argument("-e", help="Timestamp for end of query in seconds", default=0.0)
#args = parser.parse_args()

vidPath = "../IMG_6863.MOV"
s = 5.0
e = 6.5
cap = cv2.VideoCapture(vidPath)
frame_count = get_frame_count(vidPath) + 1
frame_rate = get_frame_rate(vidPath)
q_duration = float(e) - float(s)
q_total = get_duration(vidPath)

if not float(s) < float(e) < q_total:
    print 'Timestamp for end of query set to:', q_duration
    e = q_total

frames = []
query_features = []
prev_frame = None
frame_nbr = int(s)*frame_rate
cap.set(cv2.CAP_PROP_POS_MSEC, int(s)*1000)
ret, frame = cap.read()
matrix = np.zeros_like(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
matrix2 = np.zeros_like(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
while(cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < (int(e)*1000)):
    ret, frame = cap.read()
    if frame == None:
        break
            
    if not (prev_frame == None):
        res = frame - prev_frame
        res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        #cv2.imshow("eejjjjj baby", res)
        #cv2.waitKey(25)
        sec = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        matrix = matrix + sec
        frames.append(sec)
    prev_frame = frame
    frame_nbr += 10000

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#Axes3D.plot_surface(matrix)

threshold = 100
matrix2[matrix > threshold] = 255
matrix2[matrix <= threshold] = 0

#### Kernel on acc
kernel =  np.matrix('-1,-1,-1;-1,16,-1;-1,-1,-1')
kernel1 =  np.matrix('-1,-1,-1;0,0,0;1,1,1')
kernel2 =  np.matrix('-1,0,1;-1,0,1;-1,0,1')

matrix2 = convolve(matrix2, kernel)
x1 = convolve(matrix2, kernel1)
x2 = convolve(matrix2, kernel2)
res = np.sqrt(x1**2 + x2**2)
####################



#### Kernel on temp
kernelHighPass =  np.matrix('1,2,1;2,4,2;1,2,1')
kernelLowPass =  np.matrix('0.05,0.2,0.05;0.2,0.3,0.2;0.2,0.05,0.2')
kernelxDiff =  np.matrix('-1,-1,-1;0,0,0;1,1,1')
kernelyDiff =  np.matrix('-1,0,1;-1,0,1;-1,0,1')

tempp = convolve(frames[0], kernelLowPass) - frames[0]


x1 = convolve(tempp, kernelxDiff)
x2 = convolve(tempp, kernelyDiff)
res = np.sqrt((x1 + x2)^2)
####################


#x1 = convolve(convolve(tempp, kernelxDiff), kernelLowPass)
#sp.medfilt(x1,1)



#cv2.imshow("Saas", frames[0])
cv2.imshow("hoi", res)
cv2.waitKey()



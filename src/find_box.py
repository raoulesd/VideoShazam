#!/usr/bin/env python
import argparse
import numpy as np
import cv2
import glob
from scipy.io import wavfile 
import sys
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import squares as sq
  
def findBox(vidPath):
    
    s = 0.0
    e = 3.0
    cap = cv2.VideoCapture(vidPath)
    #print(frame_rate)
    cap.set(cv2.CAP_PROP_POS_MSEC, 0)
    ret, frame = cap.read()
    #cv2.imshow('x', frame)
    #cv2.waitKey()
    
    #print(frame.shape)
    videoSurface = frame.shape[0] * frame.shape[1]
    surface = 0
    
    while surface < round(videoSurface/4):
        print('hey')
        cap = cv2.VideoCapture(vidPath)
        cap.set(cv2.CAP_PROP_POS_MSEC, int(s)*1000)
        ret, frame = cap.read()
        #cv2.imshow('current frame', frame)
        #ch = cv2.waitKey()
        
        squares = sq.find_squares(frame)
        print(squares)
        videoBox = getVideoSquare(squares)[0]
        surface = (videoBox[2][0] - videoBox[0][0]) * (videoBox[2][1] - videoBox[0][1])
        
        s = s + 1.0
        
        

    #cv2.drawContours(frame, [videoBox], -1, (0, 255, 0), 3 )
    #cv2.imshow('squares', frame)
    #cv2.waitKey()
    return videoBox

    
### USED TO REMOVE THE LARGEST BOX AND RETURN THE SECOND LARGEST
def getVideoSquare(squares):
    sortedSquares = sorted(squares, key=squareSort)
    print(len(sortedSquares))
    del sortedSquares[-1]
    return [sortedSquares[-1]]

    
def getSurface(x1,y1,x2,y2):
    return (x2 - x1) * (y2 - y1)

### SORTS FROM SMALLEST SQUARE TO LARGEST
def squareSort(square):
    return getSurface(square[0][0], square[0][1], square[2][0], square[2][1])


box = findBox("../../IMG_6861.MOV")


#!/usr/bin/env python
import numpy as np
import cv2
import glob
from scipy.io import wavfile
from video_tools import *
import sys
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import squares as sq
  
def findBox(vidPath):
    
    # Pre video processing
    s = 0.0
    cap = cv2.VideoCapture(vidPath)
    frame_count = get_frame_count(vidPath) + 1
    frame_rate = np.round(get_frame_rate(vidPath))
    e = np.floor(frame_count / frame_rate)
    frame_counter = int(s)*frame_rate
    cap.set(cv2.CAP_PROP_POS_MSEC, 0)
    
    # Calculates the surface of the entire video to use later
    ret, frame = cap.read()
    videoSurface = frame.shape[0] * frame.shape[1]
    surface = 0
    
    # Define contrast variables
    maxIntensity = 255.0
    phi = 1.0
    theta = 1.0
    

    # Keeps running if the surface calculated from a square is within certain bounds
    print("Trying to find the screen. This might take a while if no clear square is found")
    while (((surface < round(videoSurface/4)) or (surface > round((videoSurface * 9)/10))) and cap.get(cv2.CAP_PROP_POS_MSEC) < (int(e)*1000)):
        
        ret, frame = cap.read()
        frame_counter = frame_counter + 1
        
        # The squares are calculated every second, since it is not a very quick algorithm and you don't need all the frames anyway.
        if  (frame_counter%frame_rate == 0.0):
            
            # Increase intensity such that dark pixels become much brighter and bright pixels become slightly bright
            cont = (maxIntensity/phi)*(frame/(maxIntensity/theta))**0.5
            cont = np.array(cont,dtype='uint8')

            # Use canny edge detection and find squares
            edges = cv2.Canny(cont, 40, 50, None, 3)
            squares = sq.find_squares(edges)
             
            if len(squares) >= 1:
                videoBox = getVideoSquare(squares, videoSurface)
                # If videoBox succeeded in a box, return it.
                if videoBox is not None:
                    surface = (videoBox[2][0] - videoBox[0][0]) * (videoBox[2][1] - videoBox[0][1])
                    return videoBox
                    
    print("square not found")        
        
          
        

    
### Removes large and small squares, and results in the final box
def getVideoSquare(squares, videoSurface):
    if len(squares)== 0:
        return None
    # Sort the squares by surface
    sortedSquares = sorted(squares, key=squareSort)
    # Take the largest one, is the safest choice
    videoBox = sortedSquares[-1]
    # If it falls outside of some bounds, delete the square and look at the next one.
    surface = abs((videoBox[2][0] - videoBox[0][0]) * (videoBox[2][1] - videoBox[0][1]))
    if ((surface < round(videoSurface/4)) or (surface > round((videoSurface * 7)/8))):
        del sortedSquares[-1]
        getVideoSquare(sortedSquares, videoSurface)
    else:
        return sortedSquares[-1]
    
def getSurface(x1,y1,x2,y2):
    return (x2 - x1) * (y2 - y1)

### Sorting method based on the surface of the squares
def squareSort(square):
    return getSurface(square[0][0], square[0][1], square[2][0], square[2][1])




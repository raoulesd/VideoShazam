#!/usr/bin/env python
import numpy as np
import progressbar
import cv2
import glob
from scipy.io import wavfile
from video_tools import *
import sys
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import squares as sq
import find_box as fb
  
def extractVideo(vidPath, skip=0):
    
    # Starting point is 0 by default
    s = 0.0
    
    # Create video capture and initialize variables
    cap = cv2.VideoCapture(vidPath)
    frame_count = get_frame_count(vidPath) + 1
    frame_rate = np.round(get_frame_rate(vidPath))
    
    # amount of seconds taken from video (5 by default for query)
    max_count = 5 * frame_rate
    
    # Progress bar code. source: https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
    bar = progressbar.ProgressBar(maxval=min(frame_count, max_count), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    
    e = round(frame_count / frame_rate)
    q_duration = float(e) - float(s)
    q_total = get_duration(vidPath)

    # finds cropping box
    videoBox = fb.findBox(vidPath)
    x1 = videoBox[0][0]
    x2 = videoBox[2][0]
    y1 = videoBox[0][1]
    y2 = videoBox[2][1]

    # Initialize variables
    frame_counter = int(s)*frame_rate
    cap.set(cv2.CAP_PROP_POS_MSEC, int(s)*1000)
    ret, frame = cap.read()
    prev_frame = None
    cropped_frames = []
    temporal_frames = []
    bar.start()

    while(cap.isOpened() and frame_counter < min(frame_count, max_count)):
        bar.update(frame_counter)
        ret, frame = cap.read()
        if frame == None:
            break
        
        # Extract cropped image from original
        cropped = frame[y1:y2, x1:x2]
        cropped_frames.append(cropped)
        
        # After having looped over two videos, prev_frame and previousTemp are not None, and entries with the second derivative are added
        if prev_frame is not None: 
            temporal = cv2.cvtColor(cropped - prev_frame, cv2.COLOR_BGR2GRAY)
            if temporal is not None:
                temporal_frames.append(sum(sum(temporal)))
        
        prev_frame = cropped
        frame_counter += 1 + skip

        
        if skip > 0:
            # This was necessary for set to work
            cap.release()
            cap = cv2.VideoCapture(vidPath)
            cap.set(cv2.CAP_PROP_POS_MSEC, frame_counter*frame_rate)
        
    bar.finish()
    return (cropped_frames, temporal_frames)



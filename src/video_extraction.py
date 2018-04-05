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
import find_box as fb
  
def extractVideo(vidPath):
        
    #vidPath = "../invention/videos/filmpie4.mp4"
    s = 0.0
    cap = cv2.VideoCapture(vidPath)
    frame_count = get_frame_count(vidPath) + 1
    frame_rate = np.round(get_frame_rate(vidPath))
    print(frame_rate)
    e = round(frame_count / frame_rate)
    print(e)
    q_duration = float(e) - float(s)
    q_total = get_duration(vidPath)

    # finds cropping box
    videoBox = fb.findBox(vidPath)
    x1 = videoBox[0][0]
    x2 = videoBox[2][0]
    y1 = videoBox[0][1]
    y2 = videoBox[2][1]

    frame_counter = int(s)*frame_rate
    cap.set(cv2.CAP_PROP_POS_MSEC, int(s)*1000)
    ret, prev_frame = cap.read()

    cropped_frames = []
    temporal_frames = []
    while(cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < (int(e)*1000)):
        ret, frame = cap.read()
        if frame == None:
            break
        cropped = frame[y1:y2, x1:x2]
        cropped_frames.append(cropped)
        
        temporal = cv2.cvtColor(frame - prev_frame, cv2.COLOR_BGR2GRAY)
        temporal_frames.append(temporal)
        
        prev_frame = frame
        frame_counter += 1
        
        #cv2.imshow('frame',temporal)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    
    
    #cap.release()

    return (cropped_frames, temporal_frames)
    
extractVideo("../../IMG_6861.MOV")



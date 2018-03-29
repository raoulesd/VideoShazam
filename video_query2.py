#!/usr/bin/env python
import argparse
import video_search
import numpy as np
import cv2
import glob
from scipy.io import wavfile
from video_tools import *
import feature_extraction as ft    
import sys
import os
from video_features import *
import matplotlib.pyplot as plt

query = "../IMG_6863.MOV"
#query = "../Videos/BlackKnight.avi"
cap = cv2.VideoCapture(query)
cap2 = cv2.VideoCapture(query)
ret, frame = cap2.read()
while(cap.isOpened() & cap2.isOpened()):
    ret, frame = cap.read()
    
    ret2, frame2 = cap2.read()
    try: 
        gray = cv2.cvtColor(frame - frame2, cv2.COLOR_BGR2GRAY)
        gray[gray < 160] = 0
    except TypeError:
        break
    cv2.imshow('frame',gray)
    cv2.waitKey(25)

cap.release()
cv2.destroyAllWindows()


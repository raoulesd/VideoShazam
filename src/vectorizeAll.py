import cv2
import glob
import sys
import numpy as np
from ast import literal_eval
import matplotlib.pyplot as plt
from video_extraction import extractVideo 
from scipy import spatial
from os import listdir
from os.path import *
from video_tools import *
import progressbar
from time import sleep

# skip n frames when creating a vector
skipFrames = 6

# relative path to database videos
path = "../database/"

# relative path to stored vectors
database = "db.npy"


def getVideoVectors(path, skip=0):        
    res = []
    print "Processing videos..."
    
    # Get all videos from file
    video_types = ('*.mp4', '*.MP4', '*.avi')
    video_list = [f for f in listdir(path) if isfile(join(path, f))]
    
    for video in video_list:
        # For each video, extract feature vector and add it to res
        res.append(getVector(path + '/' + video, skip=skip))
        print video + " done"
    return res

def getVector(path, size=25, skip=0):
    # Create video capture
    cap = cv2.VideoCapture(path)
    
    # Variable initialization
    previousFrame = None
    vector = []
    i = 0
    frameCount = get_frame_count(path) + 1
    frameRate = get_frame_rate(path)
    
    # amount of seconds taken from video (20 by default for database)
    maxCount = 15 * frameRate
    
    # Progress bar code. source: https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
    bar = progressbar.ProgressBar(maxval=min(frameCount, maxCount), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    
    
    while(cap.isOpened() and i < min(frameCount, maxCount)):
        bar.update(i)
        # Get frame of video
        ret, frame = cap.read()
        
        # After having looped over two videos, previousFrame and previousGray are not None, and entries with the second derivative are added
        if previousFrame is not None:
            gray = cv2.cvtColor(frame - previousFrame, cv2.COLOR_BGR2GRAY)
            vector.append(sum(sum(gray)))
        previousFrame = frame
        
        # Increment frame counter, including the amount of frames to be skipped
        i = i + 1 + skip
        if skip > 0:
            # Creating a new one is necesarry for set to work
            cap.release()
            cap = cv2.VideoCapture(path)
            cap.set(cv2.CAP_PROP_POS_MSEC,i*frameRate)
            
    bar.finish()
    return vector
    
# List all database videos
video_list = [f for f in listdir(path) if isfile(join(path, f))]

print "All videos:" 
print video_list

# Extract feature vectors from database
print "Creating vector database from videos in directory", path
vectors = getVideoVectors(path, skip=skipFrames)

# Write array to .npy file
print "Writing..."
np.save('db', np.array(vectors))
print "Writing succesfull!"
        










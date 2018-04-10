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

def getTopSim(sample, video, name, size=25, step=5):
    results = []
    for i in range(0, len(video) - size, step):
        subvec = video[i : i + size]
        result = 1 - spatial.distance.cosine(sample, subvec)
        results.append((result, i, name))

    results.sort(key=lambda x: x[0])
    results.reverse()
    
    print "Top 3 similarities in " + name
    for i in range(3):
        try:
            print results[i][0:2]
        except IndexError:
            break
    return results  

# skip n frames when creating a vector
skipFrames = 6

# relative path to database videos
path = "../database/"

# relative path to stored vectors
database = "db.npy"

# size of the sliding window
windowSize = 4

# queried video
query = "../ambulance.mp4"


# List all database videos
video_list = [f for f in listdir(path) if isfile(join(path, f))]

print "All videos:" 
print video_list

# Load vectors from save
vectors = []
vectors = np.load('db.npy')

# Extracts the vector of the cropped query video
print "Analyzing target video..."
video, sample = extractVideo(query, skip=skipFrames)

print "Looking for similarities from: " + query 

i = 0
res = []
for x in vectors:
    # For each video in the database, apply the sliding window over feature vector
    temp = getTopSim(sample, x, video_list[i], size = len(sample), step = windowSize)
    i = i + 1
    
    # Extend list with new entries
    res.extend(temp)

# Sort keys on similariy
res.sort(key=lambda x: x[0], reverse=True)

# Take top result and print it
print "Top result is ", res[0][2], " at ", "%.2f" % (float(res[0][1]) / 30.0), " seconds, with sim of ", "%.2f" % res[0][0]

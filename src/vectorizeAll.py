import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial
from os import listdir
from os.path import isfile, join

def getVideoVectors(path):
    res = []
    video_types = ('*.mp4', '*.MP4', '*.avi')
    video_list = [f for f in listdir(path) if isfile(join(path, f))]
    print "All videos:" 
    print video_list
    for video in video_list:
        res.append(getVector(path + '/' + video))
        print video + " done"
    return res, video_list

def getVector(path, size=25):
    cap = cv2.VideoCapture(path)
    cap2 = cv2.VideoCapture(path)
    ret2, frame2 = cap2.read()
    
    allVectors = []
    vector = []
    i = 0
    while(cap.isOpened()):# and poo < l):
        i = i + 1
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        
        try: 
            gray = cv2.cvtColor(frame - frame2, cv2.COLOR_BGR2GRAY)
        except TypeError:
            break
        vector.append(sum(sum(gray)))
        if(i % size == 0):
            allVectors.append(vector)
            vector = []
    
        #cv2.imshow('frame',gray)
        #cv2.waitKey(25)
    return np.concatenate(allVectors, axis=0)
   
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
        print results[i][0:2]
    return results
 
path = "/home/student/MMA3/toShazam/"

vectors, video_list = getVideoVectors(path)

query = "/home/student/MMA3/IMG_6863.MOV"

print "Looking for similarities in: " + query 

sample = getVector(query)

i = 0
res = []
for x in vectors:
    temp = getTopSim(sample[55:80], x, video_list[i])
    i = i + 1
    res.extend(temp)

res.sort(key=lambda x: x[0], reverse=True)
print res

print "Top result is ", res[0][2], " at ", "%.2f" % (float(res[0][1]) / 30.0), " seconds, with sim of ", res[0][0]







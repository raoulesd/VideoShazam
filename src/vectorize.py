import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

size = 25
step = 5

query = "/home/student/MMA3/IMG_6863.MOV"
#query = "../../Videos/BlackKnight.avi"
cap = cv2.VideoCapture(query)
cap2 = cv2.VideoCapture(query)

ret2, frame2 = cap2.read()

allVectors = []
vector = []
poo = 0
while(cap.isOpened()):# and poo < l):
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    poo = poo + 1
    
    try: 
        gray = cv2.cvtColor(frame - frame2, cv2.COLOR_BGR2GRAY)
    except TypeError:
        break
    vector.append(sum(sum(gray)))
    if(poo % size == 0):
        allVectors.append(vector)
        vector = []
        
    cv2.imshow('frame',gray)
    cv2.waitKey(25)
    

cv2.imshow('frame',gray)
cv2.waitKey(25)

totalVector = np.concatenate(allVectors, axis=0)

results = []
for i in range(0, len(totalVector) - size, step):
    subvec = totalVector[i : i + size]
    result = 1 - spatial.distance.cosine(allVectors[3], subvec)
    results.append((result, i))

results.sort(key=lambda x: x[0])
results.reverse()

for i in range(10):
    print results[i] 
    
plt.plot(totalVector)
plt.ylabel('some numbers')
plt.show()

cap.release()
cv2.destroyAllWindows()

def getVideoVectors(path):
    res = []
    video_types = ('*.mp4', '*.MP4', '*.avi')
    video_list = []
    for type_ in video_types:
        files = args.training_set + '/' +  type_
        video_list.extend(glob.glob(files))	
    for video in video_list:
        res.append(getVector(video))
    

def getVector(path):
    cap = cv2.VideoCapture(query)
    cap2 = cv2.VideoCapture(query)
    
    allVectors = []
    vector = []
    poo = 0
    while(cap.isOpened()):# and poo < l):
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        poo = poo + 1
        
        try: 
            gray = cv2.cvtColor(frame - frame2, cv2.COLOR_BGR2GRAY)
        except TypeError:
            break
        vector.append(sum(sum(gray)))
        if(poo % size == 0):
            allVectors.append(vector)
            vector = []
            
        cv2.imshow('frame',gray)
        cv2.waitKey(25)
    return np.concatenate(allVectors, axis=0)
   


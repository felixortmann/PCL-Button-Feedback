# -*- coding: utf-8 -*-
"""
Example code by Maximilian Schrapel

@author: Schrapel
"""

# from flask import Flask, render_template, Response
import numpy as np
import cv2


# returns center of marker
def getCenter(prev_res):
    xm=0
    ym=0
    for i in range(0,4):
        ym+=prev_res[0][0][0][i][0]
        xm+=prev_res[0][0][0][i][1]
    xm=int(xm/4)
    ym=int(ym/4)
    center = (xm,ym)
    return center

def getSize(res):
    xsize=max(abs(res[0][0][0][1][1]-res[0][0][0][2][1]),abs(res[0][0][0][3][1]-res[0][0][0][0][1]))
    ysize=max(abs(res[0][0][0][0][0]-res[0][0][0][1][0]),abs(res[0][0][0][2][0]-res[0][0][0][3][0]))
    return max(xsize,ysize)

# returns the added example emoji
def emojiOverlay(src , overlay , pos=(0,0),scale = 1):
    overlay = cv2.resize(overlay,(0,0),fx=scale,fy=scale)
    ax=0
    ay=0
    # go through image and add emoji
    # TODO: catch errors at the image corners
    for px in range(pos[0]-int(overlay.shape[0]/2),pos[0]+int(overlay.shape[0]/2)):
        for py in range(pos[1]-int(overlay.shape[1]/2),pos[1]+int(overlay.shape[1]/2)):
            if overlay[ax,ay].any()>0:
                if px>=0 and px<src.shape[0] and py>=0 and py <src.shape[1]:
                    src[px,py]=overlay[ax,ay]
            ay+=1
        ax+=1
        ay=0
    
    return src




# Opens webcam (set number according to your machine!)
cap = cv2.VideoCapture(0)

#TODO: More smileys
img_emojihappy=cv2.imread("emojihappy.png")
img_emojisad=cv2.imread("emojisad.png")
img_emojiangry=cv2.imread("emojiangry.png")
#TODO: resize depended on marker size
img_emoji=cv2.resize(img_emojiangry,(int(80),int(80)))

# stores the index of the selected emoji
imgindex = 0

# stores the previous corners of the marker
prev_res=[]

# Aruco markers
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # detect markers
    res = cv2.aruco.detectMarkers(frame,dictionary)
    
    
    # TODO add emoji selection (maybe Arduino buttons?)
    # TODO add emoji selection with keyboard numbers
    if imgindex == 0:
        img_emoji=cv2.resize(img_emojiangry,(int(80),int(80)))
    elif imgindex == 1:
        img_emoji=cv2.resize(img_emojisad,(int(80),int(80)))
    elif imgindex == 2:
        img_emoji=cv2.resize(img_emojihappy,(int(80),int(80)))
    
    
    if len(res[0]) > 0:
        for marker in res[0]:
            size_x = marker[0][0]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # For debugging: show markers
        #cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])

        # store result temporarly
        prev_res=res
        # find center position
        center=getCenter(prev_res)
        # add emoji to image
        #TODO: change size of emoji according to marker size
        scale=(getSize(prev_res)/80) * 2 
        frame=emojiOverlay(frame , img_emoji , pos=center,scale=scale)

    #TODO: make emoji motion smooth
    # elif prev_res!=[]:
        # TODO: catch unrecognized markers
        # TODO: make movement smooth and precise
        # Hint: The marker color is green, you can might detect the marker by color selections
        

    cv2.imshow('frame',frame)
    
    
    
    # press q to stop recording
    k = cv2.waitKey(1) % 256

    if k == ord('q'):
        break
    elif k == ord('a'):
        imgindex = 0
    elif k == ord('s'):
        imgindex = 1
    elif k == ord('h'):
        imgindex = 2
    else:
        continue

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
import numpy as np
import cv2
import time
import mediapipe as mp
import handTrackingModule as htm
import math

cam=cv2.VideoCapture(0)

camwid=1080
camheight=720

ptime=0
lastSnap=0

cam.set(3,camwid)
cam.set(4,camheight)

start=cv2.imread("Picture-Puzzle/start.png")

detect=htm.HandDetector()
clickPic=False
snapped=None

def overlay(background, overlay):
    alpha=0.6
    blend=cv2.addWeighted(background, 1-alpha, overlay,alpha,0)
    return blend

while True:
    succ, img=cam.read()

    if not succ:
        print("Camera is disabled")
        break

    img=cv2.flip(img,1)
    img=cv2.resize(img, (640,527))

    img=detect.findHands(img)
    handlms=[]    
    handlms2=[]

    if detect.results and detect.results.multi_hand_landmarks:
        hands=len(detect.results.multi_hand_landmarks)
        if hands>=2:
            handlms=detect.findPosition(img,handNo=0, draw=False)
            handlms2=detect.findPosition(img, handNo=1,draw=False)

    if not clickPic and len(handlms)==21 and len(handlms2)==21:
        tx1,ty1=handlms[4][1], handlms[4][2]
        tx2,ty2=handlms2[4][1], handlms2[4][2]

        fx1,fy1=handlms[8][1], handlms[8][2]
        fx2,fy2=handlms2[8][1], handlms2[8][2]
        
        cv2.rectangle(img, (tx1,ty1),(tx2,ty2),(255,0,0),4)
       
        d1=int(math.hypot(tx1-fx1,ty1-fy1))
        d2=int(math.hypot(tx2-fx2,ty2-fy2))
        # print(d1,d2)
        if d1<20 and d2<20:
            clickPic=True
            lowx,lowy=min(tx1,tx2),min(ty1,ty2)
            highx,highy=max(tx1,tx2),max(ty1,ty2)
            snapped=img[lowy:highy, lowx:highx].copy()
            lastSnap=time.time()
    
    # if clickPic:
    #     img=overlay(snapped, img)
    if clickPic and snapped is not None:
        cv2.imshow("Snapp",snapped)
    
    frame=start.copy()
    frame[120:120+527,72:72+640]=img
    
    #ctime=time.time()
    #fps=int(1/(ctime-ptime))
    #ptime=ctime
    #cv2.putText(img, f'FPS: {fps}', (10,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),2)
    cv2.imshow("Picture-Puzzle",frame)
    
    key=cv2.waitKey(1)
    if key==ord('q'):
        print("Quitting")
        break

    if key==ord('r') :
        clickPic=False
        snapped=None
    
cam.release()
cv2.destroyAllWindows()
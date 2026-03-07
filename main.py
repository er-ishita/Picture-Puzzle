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
saved=snapped

puz=None

puzHeight,puzWidth=640,527
vl1,vl2=int(puzHeight/3),int(2*puzHeight/3)
hl1,hl2=int(puzWidth/3),int(2*puzWidth/3)

def overlay(background, overlay):
    alpha=0.2
    blend=cv2.addWeighted(background, 1-alpha, overlay,alpha,0)

    h,w,_=overlay.shape
    cv2.line(blend, (0,vl1), (w-1,vl1), (0,0,0), 2)
    cv2.line(blend, (0,vl2), (w-1,vl2), (0,0,0), 2)

    cv2.line(blend, (hl1,0), (hl1,h-1), (0,0,0), 2)
    cv2.line(blend, (hl2,0), (hl2,h-1), (0,0,0), 2)

    return blend

########################################under construction
def puzzleRandom(snap):
    a11=snap[0:hl1,0:vl1]
    a12=snap[0:hl1,vl1:vl2]
    a13=snap[0:hl1,vl2:puzWidth]

    a21=snap[hl1:hl2,0:vl1]
    a22=snap[hl1:hl2,vl1:vl2]
    a23=snap[hl1:hl2,vl2:puzWidth]

    a31=snap[hl2:puzHeight,0:vl1]
    a32=snap[hl2:puzHeight,vl1:vl2]
    a33=snap[hl2:puzHeight,vl2:puzWidth]

    puzzle=np.array([
        a11,a12,a13,
        a21,a22,a23,
        a31,a32,a33
    ])

    np.random.shuffle(puzzle)

    puzzle=puzzle.reshape(3,3)
    return puzzle

def puzzleSwap(c1,c2,puzzle):
    puzzle[c1],puzzle[c2]= puzzle[c2],puzzle[c1]

###############################################################

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
            saved=snapped
            # puz=puzzleRandom(snapped)
    
    if clickPic and snapped is not None:
        h,w,_=img.shape
        snapped=cv2.resize(snapped,(640,527))
        img=overlay(snapped, img)

    if clickPic and snapped is not None:
        cv2.imshow("Snapp",snapped)
    
    frame=start.copy()
    frame[120:120+527,72:72+640]=img

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
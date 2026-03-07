import numpy as np
import cv2
import time
# import mediapipe as mp
import handTrackingModule as htm
import math

cam=cv2.VideoCapture(0)

camwid=1080
camheight=720

ptime=0
# lastSnap=0
lastSwap=0

cam.set(3,camwid)
cam.set(4,camheight)

start=cv2.imread("Picture-Puzzle/start.png")

detect=htm.HandDetector()
clickPic=False
snapped=None
saved=None

puz=None
original=None
board=None

puzHeight,puzWidth=528,642
hl1,hl2=int(puzHeight/3),int(2*puzHeight/3)
vl1,vl2=int(puzWidth/3),int(2*puzWidth/3)

def overlay(background, overlay):
    alpha=0.8
    blend=cv2.addWeighted(background, 1-alpha, overlay,alpha,0)

    h,w,_=overlay.shape

    cv2.line(blend, (0,hl1), (w-1,hl1), (0,0,0), 2)
    cv2.line(blend, (0,hl2), (w-1,hl2), (0,0,0), 2)

    cv2.line(blend, (vl1,0), (vl1,h-1), (0,0,0), 2)
    cv2.line(blend, (vl2,0), (vl2,h-1), (0,0,0), 2)

    return blend

########################################puzzle logic
def puzzleRandom(snap):

    puzHeight,puzWidth,_=snap.shape
    hl1,hl2=int(puzHeight/3),int(2*puzHeight/3)
    vl1,vl2=int(puzWidth/3),int(2*puzWidth/3)
    
    a11=snap[0:hl1,0:vl1]
    a12=snap[0:hl1,vl1:vl2]
    a13=snap[0:hl1,vl2:puzWidth]

    a21=snap[hl1:hl2,0:vl1]
    a22=snap[hl1:hl2,vl1:vl2]
    a23=snap[hl1:hl2,vl2:puzWidth]

    a31=snap[hl2:puzHeight,0:vl1]
    a32=snap[hl2:puzHeight,vl1:vl2]
    a33=snap[hl2:puzHeight,vl2:puzWidth]

    puzzle=[
        a11,a12,a13,
        a21,a22,a23,
        a31,a32,a33
    ]

    original=puzzle.copy()
    np.random.shuffle(puzzle)
    
    puzzle = [puzzle[0:3], puzzle[3:6], puzzle[6:9]]

    return puzzle,original

def getValues(pt,l1,l2):
    if pt<l1:
        return 0
    if pt<l2:
        return 1
    return 2

def puzzleSwap(x1,y1,x2,y2):
    c1=getValues(x1,vl1,vl2)
    c2=getValues(x2,vl1,vl2)
    r1=getValues(y1,hl1,hl2)
    r2=getValues(y2,hl1,hl2)
    
    puz[r1][c1],puz[r2][c2]= puz[r2][c2],puz[r1][c1]

def constructB(puz,snap):
    board = np.zeros_like(snap)

    # print("slice shape:", board[0:hl1,0:vl1].shape)
    # print("tile shape:", puz[0][0].shape)

    board[0:hl1,0:vl1] = puz[0][0]
    board[0:hl1,vl1:vl2] = puz[0][1]
    board[0:hl1,vl2:puzWidth] = puz[0][2]

    board[hl1:hl2,0:vl1] = puz[1][0]
    board[hl1:hl2,vl1:vl2] = puz[1][1]
    board[hl1:hl2,vl2:puzWidth] = puz[1][2]

    board[hl2:puzHeight,0:vl1] = puz[2][0]
    board[hl2:puzHeight,vl1:vl2] = puz[2][1]
    board[hl2:puzHeight,vl2:puzWidth] = puz[2][2]
    # print(board)
    return board

def checkpuz():
    flat=[puz[r][c] for r in range(3) for c in range(3)]
    return all(flat[i] is original[i] for i in range(9))
###############################################################

while True:
    succ, img=cam.read()

    if not succ:
        print("Camera is disabled")
        break

    img=cv2.flip(img,1)
    img=cv2.resize(img, (642,528))

    img=detect.findHands(img)
    handlms=[]    
    handlms2=[]

    ##both hand detection
    if detect.results and detect.results.multi_hand_landmarks:
        hands=len(detect.results.multi_hand_landmarks)
        
        if hands>=2:
            handlms=detect.findPosition(img,handNo=0, draw=False)
            handlms2=detect.findPosition(img, handNo=1,draw=False)
    
    ##play logic
    if clickPic and len(handlms)==21 and len(handlms2)==21:
        #thumb coordinate for both hands
        tx1,ty1=handlms[4][1], handlms[4][2]
        tx2,ty2=handlms2[4][1], handlms2[4][2]
        
        #index finger coordinate
        fx1,fy1=handlms[8][1], handlms[8][2]
        fx2,fy2=handlms2[8][1], handlms2[8][2]

        d1=int(math.hypot(tx1-fx1,ty1-fy1))
        d2=int(math.hypot(tx2-fx2,ty2-fy2))
        
        # print(d1,d2)
        ctime=time.time()
        if d1<20 and d2<20 and ctime-lastSwap>0.5:
            puzzleSwap(tx1,ty1,tx2,ty2)
            lastSwap=ctime

        if checkpuz():
            ctime=time.time()
            t=int(ctime-ptime)
            cv2.putText(saved, f"Yayy, you solved it in: {t} seconds",(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            cv2.imshow("Solved!",saved)


    ##clicking pic logic
    if not clickPic and len(handlms)==21 and len(handlms2)==21:
        
        #thumb coordinate for both hands
        tx1,ty1=handlms[4][1], handlms[4][2]
        tx2,ty2=handlms2[4][1], handlms2[4][2]
        
        #index finger coordinate
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
            snapped=cv2.resize(snapped,(642,528))

            saved=snapped.copy()
            # print("Here1")
            puz,original=puzzleRandom(snapped) 
            ptime=time.time()
            # cv2.imshow("Puzzle",board)
    
    #shuffle pic overlay
    if clickPic and puz is not None and snapped is not None:
        # print("Here2")
        # print(img.shape)
        board=constructB(puz,snapped)
        # print(board.shape)
        if img.shape != board.shape:
            board = cv2.resize(board, (img.shape[1], img.shape[0]))
        img=overlay(img,board)
    
    frame=start.copy()
    frame[120:120+528,72:72+642]=img

    cv2.imshow("Picture-Puzzle",frame)
    
    key=cv2.waitKey(1)

    if key==ord('q'):
        print("Quitting")
        break

    if key==ord('r') :
        clickPic=False
        snapped=None
        puz=None
    
cam.release()
cv2.destroyAllWindows()
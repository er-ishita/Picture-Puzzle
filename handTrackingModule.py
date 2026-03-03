import cv2
import numpy as np
import mediapipe as mp
import time

class HandDetector:
    def __init__(self, mode=False,maxHands=2,detcon=0.5,trackcon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detcon=detcon
        self.trakcon=trackcon

        self.hand=mp.solutions.hands
        self.mpHand=self.hand.Hands()
        self.mpDraw=mp.solutions.drawing_utils

        self.results=None

    def findHands(self,img, draw=True):
        # imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.mpHand.process(img)
        if self.results and self.results.multi_hand_landmarks:
            for lm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, lm, self.hand.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img,handNo=0, draw=True):
        handlms=[]
        if self.results and self.results.multi_hand_landmarks:
            hand=self.results.multi_hand_landmarks[handNo]
            h,w,_=img.shape
            for id, lm in enumerate(hand.landmark):
                cx,cy=int(lm.x*w),int(lm.y*h)
                if draw:
                    cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
                handlms.append([id,cx,cy])
        return handlms


def main():
    cam=cv2.VideoCapture(0)
    ptime=0
    htm=HandDetector()
    while True:
        succ, img=cam.read()
        
        if not succ:
            print("Camera is disabled")
            break

        img=cv2.flip(img, 1)
        img=htm.findHands(img)
        handlm=htm.findPosition(img)
        print(handlm)

        ctime=time.time()
        fps=int(1/(ctime-ptime))
        ptime=ctime

        cv2.putText(img, f'FPS: {fps}', (10,70), cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0),3)
        cv2.imshow("WebCam",img)

        if cv2.waitKey(1) & 0xff==ord('q'):
            print("Quitting")
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
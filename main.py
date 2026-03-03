import numpy as np
import cv2
import time
import mediapipe as mp
# import handTrackingModule as htm

cam=cv2.VideoCapture(0)

camwid=1080
camheight=720

ptime=0

cam.set(3,camwid)
cam.set(4,camheight)

start=cv2.imread("Picture-Puzzle\start.png")

while True:
    succ, img=cam.read()

    if not succ:
        print("Camera is disabled")
        break

    img=cv2.flip(img,1)

    img=cv2.resize(img, (640,527))

    frame=start.copy()

    frame[120:120+527,72:72+640]=img

    ctime=time.time()
    fps=int(1/(ctime-ptime))
    ptime=ctime
    cv2.putText(img, f'FPS: {fps}', (10,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),2)
    cv2.imshow("Picture-Puzzle",frame)

    if cv2.waitKey(1) & 0xff==ord('q'):
        print("Quitting")
        break
    
cam.release()
cv2.destroyAllWindows()
import cv2
import time
import numpy as np
import HandTracking as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam,hCam=1024,720
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
vol=0
detector = htm.handDetector()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

#volume.GetMasterVolumeLevel()
volumerange=volume.GetVolumeRange()

minvol=volumerange[0]
maxvol=volumerange[1]

while True:
    sucess,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img)
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),10,(0,255,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),4)
        cv2.circle(img, (cx, cy), 7, (0, 255, 255), cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        #print(length._round_(2))

        vol=np.interp(length,[10,200],[minvol,maxvol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img,(50,100),(85,400),(0,255,0),2)
        cv2.rectangle(img,(50, int(vol)), (85, 400), (0, 255, 0), 2,cv2.FILLED)
    else:
        print("No Hand Detected")



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img,f'FPS: {str(int(fps))}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2    ,
                (255, 0, 0), 3)


    cv2.imshow("Img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
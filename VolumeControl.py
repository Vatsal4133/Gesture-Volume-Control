import cv2
import keyboard
import numpy as np
import handdetectormodule as hdm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



wCam = 1920
hCam = 1080



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]



cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector =hdm.handDetector()

volbar = 0


while True:
    success, image = cap.read()
    image = detector.findHands(image)
    lmlist = detector.findPosition(image)
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2
        lenght = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(lenght, [30, 250], [minVol,maxVol])
        volbar = np.interp(lenght, [30, 300], [400, 150])
        #print(vol)
        cv2.circle(image, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(image, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x1,y1), (x2,y2), (0,0,255), 3)
        cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        if lenght<30:
            cv2.circle(image, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        cv2.rectangle(image, (50,int(volbar)), (85, 400), (0,255,0), cv2.FILLED)
    if keyboard.is_pressed('c'):
        volume.SetMasterVolumeLevel(vol, None)
    #cv2.imshow("Image", image)
    #cv2.waitKey(1)
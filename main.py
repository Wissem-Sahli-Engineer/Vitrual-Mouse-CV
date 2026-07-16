import cv2
# pyrefly: ignore [missing-import]
import mediapipe as mp 
import time 
from Hand_Tracking_Model.utils import handDetector
from utils import get_fps , draw_fps_capsule
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from pynput.mouse import Controller, Button
# pyrefly: ignore [missing-import]
from screeninfo import get_monitors

from utils import get_fingers_up


##################
""" Arguments """
##################
Wcam, Hcam = 1280 , 720 

cap = cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,Hcam)

monitor = get_monitors()[0]
Wscr , Hscr = monitor.width , monitor.height


detector = handDetector(model_path = "Hand_Tracking_Model/hand_landmarker.task",
                        num_hands = 1,
                        confidence = 0.6
                        )

mouse = Controller()

frame_count = 0
pTime = time.time()

Alert = "Hand is not completly DETECTED ! Try to move it !"

is_clicking = False
frameR = 125 
box_x1, box_y1 = frameR, frameR
box_x2, box_y2 = Wcam - frameR, Hcam - frameR

while True:

    # Reading
    test , img = cap.read()
    if not test or img is None:
        break

    # fps and time
    fps , pTime = get_fps(cap, pTime)

    timestamp_ms = int((frame_count / get_fps(cap,0,type='cap')[0]) * 1000)
    frame_count += 1

    # flipping the image Y-AXIS : 
    img = cv2.flip(img,1)

    # preprocessing
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

    res = detector.landmarker.detect_for_video(mp_img,timestamp_ms) 

    lmList = detector.findHands(img,res, draw =True, draw_finger= 8)

    cv2.rectangle(img, (box_x1, box_y1), (box_x2, box_y2), (0, 255, 0), 2)
    
    if lmList:
        lmList = lmList[0]
        f = get_fingers_up(lmList)

        x , y = lmList[8][1] , lmList[8][2]
        x , y = np.interp(x, (box_x1, box_x2), (0, Wscr)) , np.interp(y, (box_y1, box_y2), (0, Hscr))

        mouse.position = (x , y)

        if f[0] and not f[1]:
            is_clicking = False
            pass

        elif f[0] and f[1]:
            if not is_clicking:
                mouse.click(Button.left, 1)
                is_clicking = True


    else :
        cv2.putText(img,Alert, (620,100), cv2.FONT_HERSHEY_COMPLEX,
                    1, (183,81,93) , 1
                    )
        print(Alert)

    # display 
    draw_fps_capsule(img, fps)
    
    cv2.imshow('Live',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
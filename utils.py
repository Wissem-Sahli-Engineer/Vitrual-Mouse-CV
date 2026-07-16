import time , math
import cv2
# pyrefly: ignore [missing-import]
import numpy as np

# init " pTime = time.time() " before the While loop
def get_fps(cap, pTime,type='default'):
    if type == "default":
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        return fps, pTime

    elif type =="cap":
        fps= cap.get(cv2.CAP_PROP_FPS)
        if fps<= 0:
            return 30, pTime
        return fps, pTime
    else:
        return 30, pTime

def draw_fps_capsule(img, fps):
    """
    Draws a clean modern capsule for the frame-rate in the top-left corner.
    """
    fps_overlay = img.copy()
    cv2.rectangle(fps_overlay, (1175, 15), (1315, 55), (0, 0, 0), cv2.FILLED)
    cv2.addWeighted(fps_overlay, 0.5, img, 0.5, 0, img)
    cv2.putText(img, f"FPS: {int(fps)}", (1200, 42), cv2.FONT_HERSHEY_SIMPLEX, 
                0.55, (0, 255, 255), 1, cv2.LINE_AA)


def get_dist(point1,point2):
    return math.hypot(point1[1]-point2[1],point1[2]-point2[2])



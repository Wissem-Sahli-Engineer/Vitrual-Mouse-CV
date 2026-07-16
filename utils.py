import time , math
import cv2
# pyrefly: ignore [missing-import]
import numpy as np
from pynput.keyboard import Key
import subprocess

def mac_switch_desktop(direction):
    # keycode 123 is Left Arrow, 124 is Right Arrow
    keycode = 123 if direction == 'left' else 124
    script = f'tell application "System Events" to key code {keycode} using control down'
    try:
        subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    except Exception as e:
        print(f"Error switching desktop: {e}")

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


def get_fingers_up(hand):
    """Returns a list of 5 booleans: [Thumb, Index, Middle, Ring, Pinky]"""
    fingers = []

    # 4 Fingers
    for i in range(8, 21, 4):
        tip_dist = math.hypot(hand[i][1] - hand[0][1], hand[i][2] - hand[0][2])
        pip_dist = math.hypot(hand[i-2][1] - hand[0][1], hand[i-2][2] - hand[0][2])
        fingers.append(tip_dist > pip_dist)
    
    # Thumb
    thumb_tip_dist = math.hypot(hand[4][1] - hand[17][1], hand[4][2] - hand[17][2])
    thumb_ip_dist = math.hypot(hand[3][1] - hand[17][1], hand[3][2] - hand[17][2])
    fingers.append(thumb_tip_dist > thumb_ip_dist)

    return fingers

def handle_desktop_swipe(clocX, swipe_start_x, is_swiping, swipe_threshold, keyboard):

    if not is_swiping:
        is_swiping = True
        swipe_start_x = clocX 
        print(f"[Swipe] Started at x={clocX:.1f}")
    else:
        # Calculate how far the hand has moved horizontally
        distance = clocX - swipe_start_x
        print(f"[Swipe] Current x={clocX:.1f}, Start x={swipe_start_x:.1f}, Distance={distance:.1f}")

        if distance > swipe_threshold:
            print("[Swipe] Swiped Right triggered!")
            # --- MAC USERS: Swiped Right ---
            mac_switch_desktop('right')
            
            """ 
            # --- WINDOWS USERS (Uncomment below) ---
            keyboard.press(Key.ctrl)
            keyboard.press(Key.cmd) 
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            keyboard.release(Key.cmd)
            keyboard.release(Key.ctrl)
            """
            
            # Reset the start point so it doesn't rapid-fire
            swipe_start_x = clocX 
            
        elif distance < -swipe_threshold:
            print("[Swipe] Swiped Left triggered!")
            # --- MAC USERS: Swiped Left ---
            mac_switch_desktop('left')
            
            """
            # --- WINDOWS USERS (Uncomment below) ---
            keyboard.press(Key.ctrl)
            keyboard.press(Key.cmd)
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            keyboard.release(Key.cmd)
            keyboard.release(Key.ctrl)
            """
            
            # Reset the start point so it doesn't rapid-fire
            swipe_start_x = clocX
            
    return is_swiping, swipe_start_x
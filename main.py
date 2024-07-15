# The project only works with a stable version of python which can coordinate with the libraries used in the project. Thus we use "python 3.8.2"

# All the supported modules are listed below
# pip install mediapipe
# pip install opencv-python 
# pip install pyautogui 
# pip install numpy
# pip install comtypes
# pip install pycaw

import cv2
import mediapipe as mp
import numpy as np
import time
import math
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# Get screen size and initialize cursor control variables
screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0               

# Initialize audio utilities
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

last_volume_change = 0
last_action_time = 0

def hand_landmarks(image):
    results = hands.process(image)
    landmark_list = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmark_list.append([(int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])) for landmark in hand_landmarks.landmark])
    return landmark_list

def perform_actions(finger_status, current_time):
    global last_action_time
    if current_time - last_action_time < 0.2:
        return
    
    action_performed = True
    if all(finger_status):
        pyautogui.press('space')
    elif finger_status == [0, 1, 0, 0, 1]:
        pyautogui.press('right')
    elif finger_status == [0, 1, 1, 0, 1]:
        pyautogui.press('left')
    elif finger_status == [0, 1, 1, 1, 1]:
        pyautogui.press('up')
    elif finger_status == [0, 1, 1, 1, 0]:
        pyautogui.press('down')
    elif finger_status == [0, 0, 1, 0, 0]:
        pyautogui.screenshot('screenshot.png')
    else:
        action_performed = False
    
    if action_performed:
        last_action_time = current_time

def get_finger_status(landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    return [int(landmarks[tip_ids[0]][0] > landmarks[tip_ids[0] - 1][0])] + [int(landmarks[tip_id][1] < landmarks[tip_id - 2][1]) for tip_id in tip_ids[1:]]

def get_average_finger_distance(landmarks):
    if len(landmarks) >= 2:
        return (math.hypot(*(np.array(landmarks[0][20]) - np.array(landmarks[1][20]))) +
                math.hypot(*(np.array(landmarks[0][16]) - np.array(landmarks[1][16])))) / 2
    return None

# Create a named window
cv2.namedWindow("Hand Gesture Control")

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    landmarks = hand_landmarks(frame_rgb)

    current_time = time.time()

    if landmarks:
        distance = get_average_finger_distance(landmarks)
        
        if distance is not None and (current_time - last_volume_change) > 0.1:
            vol = np.interp(distance, [50, 300], [minVol, maxVol])
            volPercentage = np.interp(vol, [minVol, maxVol], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)
            last_volume_change = current_time

            volBar = int(np.interp(volPercentage, [0, 100], [720, 150]))
            cv2.rectangle(frame, (50, 150), (85, 720), (0, 255, 0), 3)
            cv2.rectangle(frame, (50, volBar), (85, 720), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(volPercentage)}%', (40, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

        if landmarks[0]:
            finger_status = get_finger_status(landmarks[0])
            perform_actions(finger_status, current_time)

            if finger_status[1] == 1 and finger_status[2] == 0:
                x1, y1 = landmarks[0][8]
                x3 = np.interp(x1, (75, 1205), (0, screen_width))
                y3 = np.interp(y1, (75, 645), (0, screen_height))

                curr_x = prev_x + (x3 - prev_x) / 8
                curr_y = prev_y + (y3 - prev_y) / 8

                pyautogui.moveTo(screen_width - curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

            if finger_status[1] == 0 and finger_status[0] == 1:
                pyautogui.click()
                time.sleep(0.3)

    cv2.imshow("Hand Gesture Control", frame)

    # Click'q' key press to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        running = False

# Clean up
cap.release()
cv2.destroyAllWindows()
print("Program terminated.")

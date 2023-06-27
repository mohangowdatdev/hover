# Silicon Sorcerers [H.O.V.E.R] - HACKMAN-6126
# Mohan Gowda T, Naga Balaji K N, Nithu Shree, Indhu Shriya

# The project only works with a stable version of python which can coordinate with the libraries used in the project. Thus we use "python 3.8.2"

# All the supported modules are listed below
# pip install mediapipe 0.10.1
# pip install opencv-python  4.7.0.72
# pip install autopy 4.0.0
# pip install numpy 1.24.3

import cv2
import mediapipe
import numpy
import autopy
import time

cap = cv2.VideoCapture(0)

initHand = mediapipe.solutions.hands  # Initializing mediapipe
# Object of mediapipe with "arguments for the hands module"
mainHand = initHand.Hands(
    min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1
)
draw = (
    mediapipe.solutions.drawing_utils
)  # Object to draw the connections between each finger index
(
    wScr,
    hScr,
) = autopy.screen.size()  # Output s the high and width of the screen (1920 x 1080)
pX, pY = 0, 0  # Previous x and y location
cX, cY = 0, 0  # Current x and y location


def handLandmarks(colorImg):
    landmarkList = []  # Default values if no landmarks are tracked

    landmarkPositions = mainHand.process(
        colorImg
    )  # Object for processing the video input
    landmarkCheck = (
        landmarkPositions.multi_hand_landmarks
    )  # Stores the out of the processing object (returns False on empty)
    if landmarkCheck:  # Checks if landmarks are tracked
        for hand in landmarkCheck:  # Landmarks for each hand
            for index, landmark in enumerate(
                hand.landmark
            ):  # Loops through the 21 indexes and outputs their landmark coordinates (x, y, & z)
                draw.draw_landmarks(
                    img, hand, initHand.HAND_CONNECTIONS
                )  # Draws each individual index on the hand with connections
                h, w, c = img.shape  # Height, width and channel on the image
                centerX, centerY = int(landmark.x * w), int(
                    landmark.y * h
                )  # Converts the decimal coordinates relative to the image for each index
                landmarkList.append(
                    [index, centerX, centerY]
                )  # Adding index and its coordinates to a list

    return landmarkList


def fingers(landmarks):
    fingerTips = []  # To store 4 sets of 1s or 0s
    tipIds = [4, 8, 12, 16, 20]  # Indexes for the tips of each finger

    # Check if thumb is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    # Check if fingers are up except the thumb
    for id in range(1, 5):
        if (
            landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]
        ):  # Checks to see if the tip of the finger is higher than the joint
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips


def controls(finger):
    if all(finger):
        return 1


def forward(finger):
    if (
        finger[3] == 0
        and finger[0] == 0
        and finger[1] == 1
        and finger[2] == 0
        and finger[4] == 1
    ):  # Code to move forward
        return 1


def backward(finger):
    if (
        finger[0] == 0
        and finger[1] == 1
        and finger[2] == 1
        and finger[3] == 0
        and finger[4] == 1
    ):  # Code to move backward
        return 1


def up(finger):
    if (
        finger[0] == 0
        and finger[1] == 1
        and finger[2] == 1
        and finger[3] == 1
        and finger[4] == 1
    ):  # Code to move up
        return 1


def down(finger):
    if (
        finger[0] == 0
        and finger[1] == 1
        and finger[2] == 1
        and finger[3] == 1
        and finger[4] == 0
    ):  # Code to move down
        return 1


while True:
    check, img = cap.read()  # Reads frames from the camera
    imgRGB = cv2.cvtColor(
        img, cv2.COLOR_BGR2RGB
    )  # Changes the format of the frames from BGR to RGB
    lmList = handLandmarks(imgRGB)
    # cv2.rectangle(img, (75, 75), (640 - 75, 480 - 75), (255, 0, 255), 2)

    if len(lmList) != 0:
        x1, y1 = lmList[8][
            1:
        ]  # Gets index 8s x and y values (skips index value because it starts from 1)
        x2, y2 = lmList[12][
            1:
        ]  # Gets index 12s x and y values (skips index value because it starts from 1)
        finger = fingers(
            lmList
        )  # Calling the fingers function to check which fingers are up

        sp = controls(finger)
        if sp == 1:
            autopy.key.tap(autopy.key.Code.SPACE)
            time.sleep(1)

        f1 = forward(finger)
        if f1 == 1:
            autopy.key.tap(autopy.key.Code.RIGHT_ARROW)
            #time.sleep(1)

        b1 = backward(finger)
        if b1 == 1:
            autopy.key.tap(autopy.key.Code.LEFT_ARROW)
            #time.sleep(1)

        u1 = up(finger)
        if u1 == 1:
            autopy.key.tap(autopy.key.Code.UP_ARROW)

        d1 = down(finger)
        if d1 == 1:
            autopy.key.tap(autopy.key.Code.DOWN_ARROW)

        if (
            finger[1] == 1 and finger[2] == 0
        ):  # Checks to see if the pointing finger is up and thumb finger is down
            x3 = numpy.interp(
                x1, (75, 640 - 75), (0, wScr)
            )  # Converts the width of the window relative to the screen width
            y3 = numpy.interp(
                y1, (75, 480 - 75), (0, hScr)
            )  # Converts the height of the window relative to the screen height

            cX = (
                pX + (x3 - pX) / 8
            )  # Stores previous x locations to update current x location
            cY = (
                pY + (y3 - pY) / 8
            )  # Stores previous y locations to update current y location

            autopy.mouse.move(
                wScr - cX, cY
            )  # Function to move the mouse to the x3 and y3 values (wSrc inverts the direction)
            pX, pY = (
                cX,
                cY,
            )  # Stores the current x and y location as previous x and y location for next loop

        if (
            finger[1] == 0 and finger[0] == 1
        ):  # Checks to see if the pointer finger is down and thumb finger is up
            autopy.mouse.click()  # Left click
            time.sleep(0.6)
    resized_img = cv2.resize(
        img, (800, 650)
    )  # Change the width and height values as per your desired size

    cv2.imshow("HOVER", resized_img)

    if cv2.waitKey(1) & 0xFF == ord("q") :
        break

import cv2
import mediapipe as mp
import math
import numpy as np
from pycaw.pycaw import AudioUtilities

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

# Volume control setup
devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

minVol, maxVol, _ = volume.GetVolumeRange()

smoothVol = minVol

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            h, w, c = img.shape

            # Thumb tip
            x1 = int(handLms.landmark[4].x * w)
            y1 = int(handLms.landmark[4].y * h)

            # Index finger tip
            x2 = int(handLms.landmark[8].x * w)
            y2 = int(handLms.landmark[8].y * h)

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)

            length = math.hypot(x2-x1, y2-y1)

            if length < 40:
                color = (0,0,255)
            else:
                color = (255,0,255)

            cv2.line(img,(x1,y1),(x2,y2),color,3)
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)

            # volume mapping
            targetVol = np.interp(length, [20,130], [minVol+10, maxVol])

            # smoothing
            smoothVol = smoothVol + (targetVol - smoothVol) * 0.2

            volume.SetMasterVolumeLevel(smoothVol, None)

            # volume bar
            volBar = np.interp(length, [20,130], [400,150])
            volPer = np.interp(length, [20,130], [0,100])

            cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
            cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)

            cv2.putText(img,f'{int(volPer)} %',(40,430),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

    cv2.imshow("Hand Gesture Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
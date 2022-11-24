from PoseModule import PoseDetector
import Globaluse
import cv2
import numpy as np

cap = cv2.VideoCapture("./Project/Test_Media/Jumping_Jacks.mp4")

if not cap.isOpened():
    print("Cannot open video")
    exit()

'''
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
'''  

detector = PoseDetector()
dir = 1  # 0: 開 1: 合
count = 0

while True:
    success, img = cap.read()

    if success:
        pose, img = detector.findPose(img, draw=True)

        if pose:
            lmList = pose["lmList"]
            angle1, img = detector.findAngle(lmList[14], lmList[12],
                                             lmList[24], img)
            angle2, img = detector.findAngle(lmList[26], lmList[24],
                                             lmList[23], img)

            # 顯示進度條
            Globaluse.thebar(img, angle2, 80, 100)

            # 目前狀態::開
            if angle2 <= 90 and angle2 >= 70 and angle1 >= 0 and angle1 <= 30:
                if dir == 0:   # 之前狀態:開
                    count = count + 0.5
                    dir = 1    # 更新狀態:合

            # 目前狀態::合
            if angle2 <= 110 and angle2 >= 90 and angle1 >= 160 and angle1 <= 180:
                if dir == 1:   # 之前狀態:合
                    count = count + 0.5
                    dir = 0    # 更新狀態:開

            Globaluse.thecount(img, str(int(count)))

        cv2.imshow("Pose", img)

    else:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
from PoseModule import PoseDetector
import Globaluse
import cv2
import numpy as np

cap = cv2.VideoCapture("./Project/Test_Media/Push_Up.mp4") #使用影片

if not cap.isOpened():
    print("Cannot open vedio")
    exit()

'''
cap = cv2.VideoCapture(0) #使用攝像頭

if not cap.isOpened():
    print("Cannot open camera")
    exit()
'''

detector = PoseDetector()
dir = 0  # 0: 挺身 1: 伏地
count = 0

while True:
    success, img = cap.read()

    if success:
        h, w, c = img.shape
        pose, img = detector.findPose(img, draw=True)

        if pose:
            lmList = pose["lmList"]
            angle1, img = detector.findAngle(lmList[11], lmList[23],
                                             lmList[25], img)
            angle2, img = detector.findAngle(lmList[11], lmList[13],
                                             lmList[15], img)

            # 顯示進度條
            Globaluse.thebar(img, angle2, 60, 175)
            print(int(angle1), int(angle2))

            # 目前狀態::伏地
            if angle2 <= 110 and angle1 >= 165 and angle1 <= 180:
                if dir == 0:   # 之前狀態:挺身
                    count = count + 0.5
                    dir = 1    # 更新狀態:伏地

            # 目前狀態::挺身
            if angle2 >= 160 and angle1 >= 150 and angle1 <= 180:
                if dir == 1:   # 之前狀態:伏地
                    count = count + 0.5
                    dir = 0    # 更新狀態:挺身

            Globaluse.thetext(img, str(int(count)))

        cv2.imshow("Pose", img)

    else:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
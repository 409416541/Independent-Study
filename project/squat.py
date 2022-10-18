from PoseModule import PoseDetector
import globaluse
import cv2
import numpy as np

'''
cap = cv2.VideoCapture("./reference/code/media/Squat.mp4")
'''

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
detector = PoseDetector()
dir = 0  # 0: 站起  1: 蹲下
count = 0
while True:
    success, img = cap.read()
    if success:
        h, w, c = img.shape
        pose, img = detector.findPose(img, draw=True)
        if pose:
            lmList = pose["lmList"]
            angle, img = detector.findAngle(lmList[24], lmList[26],
                                            lmList[28], img)
            # 顯示進度條
            globaluse.thebar(img, angle, 95, 175)
            if angle <= 110:  # 目前狀態:蹲下
                if dir == 0:  # 之前狀態:站起
                    count = count + 0.5
                    dir = 1   # 更新狀態:蹲下
            if angle >= 165:  # 目前狀態:站起
                if dir == 1:  # 之前狀態:蹲下
                    count = count + 0.5
                    dir = 0   # 更新狀態:站起
            globaluse.thetext(img, str(int(count)))
        cv2.imshow("Pose", img)        
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


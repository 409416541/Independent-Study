from PoseModule import PoseDetector
import Globaluse
import cv2

cap = cv2.VideoCapture("./Project/Test_Media/leg_raises.mp4")

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
dir = 1  # 0: 抬腿 1: 躺著
count = 0

while True:
    success, img = cap.read()

    if success:
        pose, img = detector.findPose(img, draw=True)

        if pose:
            lmList = pose["lmList"]
            angle1, img = detector.findAngle(lmList[12], lmList[24],
                                             lmList[26], img)
            angle2, img = detector.findAngle(lmList[24], lmList[26],
                                             lmList[28], img)

            # 顯示進度條
            Globaluse.thebar(img, angle1, 90, 180)

            # 目前狀態::抬腿
            if angle2 <= 180 and angle2 >= 155 and angle1 >= 155 and angle1 <= 180:
                if dir == 0:   # 之前狀態:抬腿
                    count = count + 0.5
                    dir = 1    # 更新狀態:躺著

            # 目前狀態::躺著
            if angle2 <= 180 and angle2 >= 155 and angle1 >= 75 and angle1 <= 90:
                if dir == 1:   # 之前狀態:躺著
                    count = count + 0.5
                    dir = 0    # 更新狀態:抬腿

            Globaluse.thecount(img, str(int(count)))

        cv2.imshow("Pose", img)

    else:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
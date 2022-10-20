from PoseModule import PoseDetector
import cv2
import numpy as np

cap = cv2.VideoCapture("media/Push_Up.mp4")
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
            bar = np.interp(angle2, (60, 175), (w//2-100, w//2+100))
            cv2.rectangle(img, (w//2-100, h-150), (int(bar), h-100),
                               (0, 255, 0), cv2.FILLED)
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
            msg = str(int(count))         
            cv2.putText(img, msg, (w-150, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        5, (255, 0, 255), 20)
        cv2.imshow("Pose", img)
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

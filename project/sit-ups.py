from PoseModule import PoseDetector
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
detector = PoseDetector()
dir = 0  # 0: 仰臥 1: 起坐
count = 0
while True:
    success, img = cap.read()
    if success:
        h, w, c = img.shape
        pose, img = detector.findPose(img, draw=True)
        if pose:
            lmList = pose["lmList"]
            angle, img = detector.findAngle(lmList[12], lmList[24],
                                            lmList[26], img)
            # 顯示進度條
            bar = np.interp(angle, (20, 100), (w//2-100, w//2+100))
            cv2.rectangle(img, (w//2-100, h-150), (int(bar), h-100),
                               (0, 255, 0), cv2.FILLED)
            if angle <= 50:   # 目前狀態:起坐
                if dir == 0:  # 之阱狀態:仰臥
                    count = count + 0.5
                    dir = 1   # 更新狀態:起坐
            if angle >= 90:   # 目前狀態:仰臥
                if dir == 1:  # 之前狀態:起坐
                    count = count + 0.5
                    dir = 0   # 更新狀態:仰臥
            msg = str(int(count))        
            cv2.putText(img, msg, (w-150, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        5, (255, 255, 255), 20)
        cv2.imshow("Pose", img)
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

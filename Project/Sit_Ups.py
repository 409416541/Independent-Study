from PoseModule import PoseDetector
import Global_Use
import cv2

'''
cap = cv2.VideoCapture('./Project/Test_Media/Sit_Up.mp4')

if not cap.isOpened():
    print("Cannot open video")
    exit()  
'''  

'''
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
'''

dir = 0  # 0: 仰臥 1: 起坐
count = 0

def Pose_Detected(cap, use_vedio, dir, count):

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Sit_Up.mp4')

        if not cap.isOpened():
            print("Cannot open video")
            exit()  

    detector = PoseDetector()

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                angle, img = detector.findAngle(landmarks[12], landmarks[24],
                                                landmarks[26], img)

                # 顯示進度條
                Global_Use.thebar(img, angle, 20, 100)

                if angle <= 50:   # 目前狀態:起坐
                    if dir == 0:  # 之阱狀態:仰臥
                        count = count + 0.5
                        dir = 1   # 更新狀態:起坐

                if angle >= 90:   # 目前狀態:仰臥
                    if dir == 1:  # 之前狀態:起坐
                        count = count + 0.5
                        dir = 0   # 更新狀態:仰臥

                Global_Use.thecount(img, str(int(count)))

            if(not use_vedio):
                return dir, count, img

            else:
                cv2.imshow('Sit Ups', img)

        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir , count)

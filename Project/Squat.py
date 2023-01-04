from PoseModule import PoseDetector
import Global_Use
import cv2

'''
cap = cv2.VideoCapture('./Project/Test_Media/Squat.mp4')

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

dir = 0  # 0: 站起  1: 蹲下
count = 0

def Pose_Detected(cap, use_vedio, dir, count):

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Squat.mp4')

        if not cap.isOpened():
            print("Cannot open video")
            exit()  

    detector = PoseDetector()

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                angle, img = detector.findAngle(landmarks[24], landmarks[26],
                                                landmarks[28], img)
                                                
                # 顯示進度條
                Global_Use.thebar(img, angle, 95, 175)

                if angle <= 110:  # 目前狀態:蹲下
                    if dir == 0:  # 之前狀態:站起
                        count = count + 0.5
                        dir = 1   # 更新狀態:蹲下

                if angle >= 165:  # 目前狀態:站起
                    if dir == 1:  # 之前狀態:蹲下
                        count = count + 0.5
                        dir = 0   # 更新狀態:站起
                        
                Global_Use.thecount(img, str(int(count)))

            if(not use_vedio):
                return dir, count, img

            else:
                cv2.imshow('Squat', img)    

        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir , count)

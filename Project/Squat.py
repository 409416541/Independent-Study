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
                angle1_1, img = detector.findAngle(landmarks[12], landmarks[24],
                                                landmarks[26], img)
                angle1_2, img = detector.findAngle(landmarks[11], landmarks[23],
                                                landmarks[25], img)
                angle2_1, img = detector.findAngle(landmarks[24], landmarks[26],
                                                landmarks[28], img)
                angle2_2, img = detector.findAngle(landmarks[23], landmarks[25],
                                                landmarks[27], img)
                angle3_1, img = detector.findAngle(landmarks[26], landmarks[24],
                                                landmarks[23], img)
                angle3_2, img = detector.findAngle(landmarks[24], landmarks[23],
                                                landmarks[25], img)
                                                
                # 顯示進度條
                Global_Use.thebar(img, angle2_1, 85, 175)
                
                if 80 <= angle1_1 <= 180 and 80 <= angle1_2 <= 180 \
                    and 80 <= angle2_1 <= 180 and 80 <= angle2_2 <= 180 \
                    and 80 <= angle3_1 <= 135 and 80 <= angle3_2 <= 135:

                    if dir == 0:  # 之前狀態:站起
                        if 80 <= angle1_1 <=100 and 80 <= angle1_2 <= 100 \
                            and 80 <= angle2_1 <= 100 and 80 <= angle2_2 <= 100:  # 目前狀態:蹲下
                            count = count + 0.5
                            dir = 1   # 更新狀態:蹲下

                    if dir == 1:  # 之前狀態:蹲下
                        if 160 <= angle1_1 <=180 and 160 <= angle1_2 <= 180 \
                            and 160 <= angle2_1 <= 180 and 160 <= angle2_2 <= 180:  # 目前狀態:站起
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
#Pose_Detected(cap, 0, dir , count)

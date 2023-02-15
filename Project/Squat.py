from PoseModule import PoseDetector
import Global_Use
import cv2


cap = cv2.VideoCapture('./Project/Test_Media/Squat.mp4')

if not cap.isOpened():
    print("Cannot open video")
    exit()  
 


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


dir = 0  # 0: 站起  1: 蹲下
count = 0

def Pose_Detected(cap, use_vedio, dir, count):

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Squat.mp4')

        if not cap.isOpened():
            print("Cannot open video")
            exit()  

    detector = PoseDetector()

    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    accuracy = 0 
    angle_top = 185

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                #angle1:肩膀到髖到膝蓋的角度
                angle1_1, img = detector.findAngle(landmarks[12], landmarks[24],
                                                landmarks[26], img)
                angle1_2, img = detector.findAngle(landmarks[11], landmarks[23],
                                                landmarks[25], img)
                #angle2:髖到膝蓋到腳踝的角度
                angle2_1, img = detector.findAngle(landmarks[24], landmarks[26],
                                                landmarks[28], img)
                angle2_2, img = detector.findAngle(landmarks[23], landmarks[25],
                                                landmarks[27], img)
                '''
                #angle3:髖到髖到膝蓋的角度
                angle3_1, img = detector.findAngle(landmarks[26], landmarks[24],
                                                landmarks[23], img)
                angle3_2, img = detector.findAngle(landmarks[24], landmarks[23],
                                                landmarks[25], img)
                '''
                                                
                # 顯示進度條
                Global_Use.thebar(img, angle1_1, 90, 175)
                
                # 正確姿勢的範圍
                if 70 <= angle1_1 <= 180 and 70 <= angle1_2 <= 180 \
                    and 80 <= angle2_1 <= 180 and 80 <= angle2_2 <= 180:

                    # 目前狀態:蹲下
                    if dir == 0:  # 之前狀態:站起
                        if 71 <= angle1_1 <=110 and 71 <= angle1_2 <= 110 \
                            and 81 <= angle2_1 <= 110 and 81 <= angle2_2 <= 110:

                            # angle_top:角度極值
                            if angle_top > (angle1_1 + angle1_2)/2:
                                angle_top = (angle1_1 + angle1_2)/2

                            if angle_top < (angle1_1 + angle1_2)/2 and (angle1_1 + angle1_2)/2 - angle_top > 5:
                                count = count + 0.5
                                dir = 1    # 更新狀態:蹲下

                    # 目前狀態:站起
                    if dir == 1:  # 之前狀態:蹲下
                        if 156 <= angle1_1 <=180 and 156 <= angle1_2 <= 180 \
                            and 161 <= angle2_1 <= 180 and 161 <= angle2_2 <= 180:

                            accuracy = 100 - 1 * abs(angle_top - 85)    # 更新正確度
                            angle_top = 180
                            count = count + 0.5
                            dir = 0   # 更新狀態:站起
                        
                Global_Use.thecount(img, str(int(count)))
                Global_Use.accuracy(img, str(int(accuracy)) + ' %', imgc)

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

Pose_Detected(cap, 1, dir , count)
Pose_Detected(cap, 0, dir , count)
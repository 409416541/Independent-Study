from PoseModule import PoseDetector
import Global_Use
import cv2


cap = cv2.VideoCapture('./Project/Test_Media/leg_raises.mp4')

if not cap.isOpened():
    print("Cannot open video")
    exit()  



cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


dir = 1  # 0: 抬腿 1: 躺著
count = 0

def Pose_Detected(cap, use_vedio, dir, count):

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/leg_raises.mp4')

        if not cap.isOpened():
            print("Cannot open camera")
            exit()

    detector = PoseDetector()

    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    accuracy_x = 0 
    accuracy_y = 0

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                angle1_1, img = detector.findAngle(landmarks[14], landmarks[12],
                                                landmarks[24], img)
                angle1_2, img = detector.findAngle(landmarks[13], landmarks[11],
                                                landmarks[23], img)
                angle2_1, img = detector.findAngle(landmarks[12], landmarks[24],
                                                landmarks[26], img)
                angle2_2, img = detector.findAngle(landmarks[11], landmarks[23],
                                                landmarks[25], img)
                angle3_1, img = detector.findAngle(landmarks[24], landmarks[26],
                                                landmarks[28], img)
                angle3_2, img = detector.findAngle(landmarks[23], landmarks[25],
                                                landmarks[27], img)
                angle4_1, img = detector.findAngle(landmarks[12], landmarks[14],
                                                landmarks[16], img)
                angle4_2, img = detector.findAngle(landmarks[11], landmarks[13],
                                                landmarks[15], img)
                '''
                angle5_1, img = detector.findAngle(landmarks[23], landmarks[24],
                                                landmarks[26], img)
                angle5_2, img = detector.findAngle(landmarks[24], landmarks[23],
                                                landmarks[25], img)
                '''

                # 顯示進度條
                Global_Use.thebar(img, angle2_1, 90, 180)

                if 0 <= angle1_1 <= 20 and 0 <= angle1_2 <= 20 \
                    and 70 <= angle2_1 <= 180 and 70 <= angle2_2 <= 180 \
                    and 160 <= angle3_1 <= 180 and 160 <= angle3_2 <= 180 \
                    and 160 <= angle4_1 <= 180 and 160 <= angle4_2 <= 180:

                    # 目前狀態::抬腿
                    if dir == 0:# 之前狀態:抬腿
                        if 160 <= angle2_1 <= 180 and 160 <= angle2_2 <= 180:
                            count = count + 0.5
                            dir = 1    # 更新狀態:躺著
                            accuracy_y = 0
                    
                    # 目前狀態::躺著
                    if 76 <= angle2_1 <= 95 and 76 <= angle2_2 <= 95:
                        while dir == 1:   # 之前狀態:躺著
                            if angle2_2 >= 96:
                                count = count + 0.5
                                dir = 0    # 更新狀態:抬腿
                            else:
                                if 76 <= angle2_1 <= 80 and 76 <= angle2_2 <= 80:
                                    accuracy_y = 100
                                else:
                                    if 81 <= angle2_1 <= 85 and 81 <= angle2_2 <= 85:
                                        accuracy_y = 90
                                    else:
                                        if 86 <= angle2_1 <= 90 and 86 <= angle2_2 <= 90:
                                            accuracy_y = 75
                                        else:
                                            if 91 <= angle2_1 <= 95 and 91 <= angle2_2 <= 95:
                                                accuracy_y = 60
                            
                accuracy = accuracy_y
                Global_Use.thecount(img, str(int(count)))
                Global_Use.accuracy(img, str(int(accuracy)) + ' %', imgc)

            if(not use_vedio):
                return dir, count, img

            else:
                cv2.imshow('Leg Raises', img)
                
        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

Pose_Detected(cap, 1, dir , count)
Pose_Detected(cap, 0, dir , count)

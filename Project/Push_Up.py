from PoseModule import PoseDetector
import Global_Use
import cv2


cap = cv2.VideoCapture('./Project/Test_Media/Push_Up.mp4')

if not cap.isOpened():
    print("Cannot open video")
    exit()  



cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


dir = 0  # 0: 挺身 1: 伏地
count = 0

def Pose_Detected(cap, use_vedio, dir, count):

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Push_Up.mp4')
        
        if not cap.isOpened():
            print("Cannot open video")
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
                #angle1:肩膀到手肘到手腕的角度
                angle1_1, img = detector.findAngle(landmarks[11], landmarks[13],
                                                landmarks[15], img)
                angle1_2, img = detector.findAngle(landmarks[12], landmarks[14],
                                                landmarks[16], img)
                #angle2:髖到肩膀到手肘的角度
                angle2_1, img = detector.findAngle(landmarks[13], landmarks[11],
                                                landmarks[23], img)
                angle2_2, img = detector.findAngle(landmarks[14], landmarks[12],
                                                landmarks[24], img)
                #angle3:肩膀到髖到膝蓋的角度
                angle3_1, img = detector.findAngle(landmarks[11], landmarks[23],
                                                landmarks[25], img)
                angle3_2, img = detector.findAngle(landmarks[12], landmarks[24],
                                                landmarks[26], img)
                #angle4:髖到膝蓋到腳踝
                angle4_1, img = detector.findAngle(landmarks[23], landmarks[25],
                                                landmarks[27], img)
                angle4_2, img = detector.findAngle(landmarks[24], landmarks[26],
                                                landmarks[28], img)

                # 顯示進度條
                Global_Use.thebar(img, angle1_1, 60, 175)
                if 160 <= angle3_1 <= 180 and 160 <= angle3_2 <= 180 \
                    and 160 <= angle4_1 <= 180 and 160 <= angle4_2 <= 180:

                    if dir == 0:   # 之前狀態:挺身
                        if 51 <= angle1_1 <= 70 and 51 <= angle1_2 <= 70: # 目前狀態::伏地
                            count = count + 0.5
                            dir = 1    # 更新狀態:伏地
                            accuracy_x = 100
                            
                        else:
                            if 61 <= angle1_1 <= 70 and 61 <= angle1_2 <= 70:
                                accuracy_x = 90
                            else:
                                if 71 <= angle1_1 <= 80 and 71 <= angle1_2 <= 80:
                                    accuracy_x = 75
                                else:
                                    if 81 <= angle1_1 <= 90 and 81 <= angle1_2 <= 90:
                                        accuracy_x = 60
                                    
                    if dir == 1:   # 之前狀態:伏地
                        if 161 <= angle1_1 <= 170 and 161 <= angle1_2 <= 170: # 目前狀態::挺身
                            accuracy_y = 100
                            count = count + 0.5
                            dir = 0    # 更新狀態:挺身
                        else:
                            if 151 <= angle1_1 <= 160 and 151 <= angle1_2 <= 160:
                                accuracy_y = 90
                            else:
                                if 141 <= angle1_1 <= 150 and 141 <= angle1_2 <= 150:
                                    accuracy_y = 75
                                else:
                                    if 131 <= angle1_1 <= 140 and 131 <= angle1_2 <= 140:
                                        accuracy_y = 60
                                        
                accuracy = (accuracy_x+accuracy_y)/2
                Global_Use.thecount(img, str(int(count)))
                Global_Use.accuracy(img, str(int(accuracy)) + ' %', imgc)

            if(not use_vedio):
                return dir, count, img

            else:
                cv2.imshow('Push Up', img)

        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

Pose_Detected(cap, 1, dir , count)
Pose_Detected(cap, 0, dir , count)

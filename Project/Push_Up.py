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

    accuracy = 0 
    angle_top = 100

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

                # 正確姿勢的範圍
                if 160 <= angle3_1 <= 180 and 160 <= angle3_2 <= 180 \
                    and 160 <= angle4_1 <= 180 and 160 <= angle4_2 <= 180:

                    # 目前狀態::伏地
                    if dir == 0:   # 之前狀態:挺身
                        if 56 <= angle1_1 <= 85 and 56 <= angle1_2 <= 85:

                            # angle_top:角度極值
                            if angle_top > (angle1_1 + angle1_2)/2:
                                angle_top = (angle1_1 + angle1_2)/2

                            if angle_top < (angle1_1 + angle1_2)/2 and (angle1_1 + angle1_2)/2 - angle_top > 5:
                                count = count + 0.5
                                dir = 1    # 更新狀態:伏地

                    # 目前狀態::挺身
                    if dir == 1:   # 之前狀態:伏地
                        if 161 <= angle1_1 <= 180 and 161 <= angle1_2 <= 180:

                            accuracy = 100 - 2.5 * abs(angle_top - 60)    # 更新正確度
                            angle_top = 180
                            count = count + 0.5
                            dir = 0    # 更新狀態:挺身
                
                
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

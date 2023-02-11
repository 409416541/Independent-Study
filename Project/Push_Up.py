from PoseModule import PoseDetector
import Global_Use
import cv2

'''
cap = cv2.VideoCapture('./Project/Test_Media/Push_Up.mp4')

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

dir = 0  # 0: 挺身 1: 伏地
count = 0

def Pose_Detected(cap, use_vedio, dir, count):

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Push_Up.mp4')
        
        if not cap.isOpened():
            print("Cannot open video")
            exit()  

    detector = PoseDetector()

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                #angle1:肩膀到髖到膝蓋的角度
                angle1_1, img = detector.findAngle(landmarks[11], landmarks[23],
                                                landmarks[25], img)
                angle1_2, img = detector.findAngle(landmarks[12], landmarks[24],
                                                landmarks[26], img)
                #angle2:肩膀到手肘到手腕的角度
                angle2_1, img = detector.findAngle(landmarks[11], landmarks[13],
                                                landmarks[15], img)
                angle2_2, img = detector.findAngle(landmarks[12], landmarks[14],
                                                landmarks[16], img)

                # 顯示進度條
                Global_Use.thebar(img, angle2, 60, 175)

                # 目前狀態::伏地
                if angle2 <= 110 and 165 <= angle1 <= 180:
                    if dir == 0:   # 之前狀態:挺身
                        count = count + 0.5
                        dir = 1    # 更新狀態:伏地

                # 目前狀態::挺身
                if angle2 >= 160 and 150 <= angle1 <= 180:
                    if dir == 1:   # 之前狀態:伏地
                        count = count + 0.5
                        dir = 0    # 更新狀態:挺身

                Global_Use.thecount(img, str(int(count)))

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

#Pose_Detected(cap, 1, dir , count)
#Pose_Detected(cap, 0, dir , count)

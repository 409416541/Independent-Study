from PoseModule import PoseDetector
import Global_Use
import cv2
import winsound
import pygame  

'''  

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

'''
 
dir = 0  # 0: 仰臥 1: 起坐
count = 0
accuracy = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Sit_ups_sample.mp4')

        if not cap.isOpened():
            print("Cannot open video")
            exit()  

    detector = PoseDetector()

    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    accuracy = 0 
    angle_top = 180

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                #肩膀到髖到膝蓋
                angle1_1, img = detector.findAngle(landmarks[12], landmarks[24],
                                                landmarks[26], img)
                angle1_2, img = detector.findAngle(landmarks[11], landmarks[23],
                                                landmarks[25], img)
                #髖到膝蓋到腳踝
                angle2_1, img = detector.findAngle(landmarks[24], landmarks[26],
                                                landmarks[28], img)
                angle2_2, img = detector.findAngle(landmarks[23], landmarks[25],
                                                landmarks[27], img)
                #肩膀到手肘到手腕
                angle3_1, img = detector.findAngle(landmarks[12], landmarks[14],
                                                landmarks[16], img)
                angle3_2, img = detector.findAngle(landmarks[11], landmarks[13],
                                                landmarks[15], img)
                #手肘到肩膀到髖
                angle4_1, img = detector.findAngle(landmarks[14], landmarks[12],
                                                landmarks[24], img)
                angle4_2, img = detector.findAngle(landmarks[13], landmarks[11],
                                                landmarks[23], img)
                # 顯示進度條
                Global_Use.thebar(img, angle1_1, 85, 125)

                # 正確姿勢的範圍
                if 50 <= angle2_1 <= 80 and 50 <= angle2_2 <= 80 \
                    and 130 <= angle3_1 <= 180 and 130 <= angle3_2 <= 180 \
                    and 40 <= angle4_1 <= 90 and 40 <= angle4_2 <= 90:

                    # 目前狀態:起坐
                    if dir == 0:  # 之前狀態:躺著
                        if  66 <= (angle1_1 + angle1_2)/2 <= 105:
                            
                             # angle_top:角度極值
                            if angle_top > (angle1_1 + angle1_2)/2:
                                angle_top = (angle1_1 + angle1_2)/2

                            if angle_top < (angle1_1 + angle1_2)/2 and (angle1_1 + angle1_2)/2 - angle_top > 5:
                                count = count + 0.5
                                dir = 1    # 更新狀態:起坐

                    # 目前狀態:躺著
                    if dir == 1:  # 之前狀態:起坐
                        if (angle1_1 + angle1_2)/2 >= 105:

                            accuracy = 100 - 2 * abs(angle_top - 85)    # 更新正確度
                            angle_top = 180
                            count = count + 0.5
                            dir = 0   # 更新狀態:躺著

                            if count % 1 == 0:
                                    pygame.mixer.init()
                                    pygame.mixer.music.load('./Project/Test_Media/sound.wav')
                                    pygame.mixer.music.play()
                                    #winsound.PlaySound("./Project/Test_Media/sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )

            if(accuracy<60):
                Global_Use.sport1(img, str(int(count)), 'Out of Range', text, imgc, imgr)
            else:
                Global_Use.sport(img, str(int(count)), str(int(accuracy)) + ' %', text, imgc, imgr)
                
            if(not use_vedio):
                return dir, count, img, accuracy

            else:
                cv2.imshow('Sit Ups', img)

        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir , count, 'Sit Ups', accuracy)
#Pose_Detected(cap, 0, dir , count, 'Sit Ups', accuracy)

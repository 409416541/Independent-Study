from PoseModule import PoseDetector
import Global_Use
import cv2
import winsound
import pygame
import pyttsx3

'''

engine = pyttsx3.init()
engine.setProperty('rate', 160)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")

    engine.say('Cannot open camera')
    engine.runAndWait()
            
    exit()

'''


cap = 0
dir = 0  # 0: 抬腿 1: 躺著
count = 0
accuracy = 0
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Leg_raises.mp4')

        if not cap.isOpened():
            print("Cannot open camera")

            engine.say('Cannot open camera')
            engine.runAndWait()

            exit()

    detector = PoseDetector()

    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    accuracy = 0 
    angle_top = 180

    while True:
        img = cap.read()[1]

        landmarks, img = detector.findPose(img, draw=True)

        #angle1:手肘到肩膀到寬的角度
        angle1_1, img = detector.findAngle(landmarks[14], landmarks[12],
                                        landmarks[24], img)
        angle1_2, img = detector.findAngle(landmarks[13], landmarks[11],
                                        landmarks[23], img)
        
        #angle2:肩膀到髖到膝蓋的角度
        angle2_1, img = detector.findAngle(landmarks[12], landmarks[24],
                                        landmarks[26], img)
        angle2_2, img = detector.findAngle(landmarks[11], landmarks[23],
                                        landmarks[25], img)
        
        #angle3:髖到膝蓋到腳踝的角度
        angle3_1, img = detector.findAngle(landmarks[24], landmarks[26],
                                        landmarks[28], img)
        angle3_2, img = detector.findAngle(landmarks[23], landmarks[25],
                                        landmarks[27], img)
        
        #angle4:肩膀到手肘到手腕的角度
        angle4_1, img = detector.findAngle(landmarks[12], landmarks[14],
                                        landmarks[16], img)
        angle4_2, img = detector.findAngle(landmarks[11], landmarks[13],
                                        landmarks[15], img)
        '''
        #angle5:髖到髖到膝蓋的角度
        angle5_1, img = detector.findAngle(landmarks[23], landmarks[24],
                                        landmarks[26], img)
        angle5_2, img = detector.findAngle(landmarks[24], landmarks[23],
                                        landmarks[25], img)
        '''

        # 顯示進度條
        Global_Use.thebar(img, angle2_1, 90, 180)

        # 正確姿勢的範圍
        if 0 <= angle1_1 <= 32 and 0 <= angle1_2 <= 32 \
            and 70 <= angle2_1 <= 180 and 70 <= angle2_2 <= 180 \
            and 155 <= angle3_1 <= 180 and 155 <= angle3_2 <= 180 \
            and 160 <= angle4_1 <= 180 and 160 <= angle4_2 <= 180:
                            
            # 目前狀態::抬腿
            if dir == 0:   # 之前狀態:躺著
                if 76 <= angle2_1 <= 95 and 76 <= angle2_2 <= 95:

                    # angle_top:角度極值
                    if angle_top > (angle2_1 + angle2_2)/2:
                        angle_top = (angle2_1 + angle2_2)/2

                    
                    if angle_top < (angle2_1 + angle2_2)/2 and (angle2_1 + angle2_2)/2 - angle_top > 5:
                        count = count + 0.5
                        dir = 1    # 更新狀態:抬腿      

            # 目前狀態::躺著
            if dir == 1:# 之前狀態:抬腿
                if 161 <= angle2_1 <= 180 and 161 <= angle2_2 <= 180:

                    accuracy = 100 - 2.5 * abs(angle_top - 80)    # 更新正確度
                    angle_top = 180
                    count = count + 0.5
                    dir = 0    # 更新狀態:躺著
                    if count % 1 == 0:
                            pygame.mixer.init()
                            pygame.mixer.music.load('./Project/Test_Media/sound.wav')
                            pygame.mixer.music.play()
                            #winsound.PlaySound("./Project/Test_Media/sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )        
        
        if(accuracy<62.5):
            Global_Use.sport1(img, str(int(count)), 'Out of Range', text, imgc, imgr)
            
        else:
            Global_Use.sport(img, str(int(count)), str(int(accuracy)) + ' %', text, imgc, imgr)

        if(use_vedio or internal_test):
            cv2.imshow('Leg Raises', img)

        else:
            return dir, count, img, accuracy

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir , count, 'Leg Raises', accuracy)
#internal_test = 1
#Pose_Detected(cap, 0, dir , count, 'Leg Raises', accuracy)

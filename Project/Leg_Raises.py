from PoseModule import PoseDetector
import Global_Use
import cv2
import pygame
import pyttsx3



engine = pyttsx3.init()
engine.setProperty('rate', 160)

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")

    engine.say('Cannot open camera')
    engine.runAndWait()
            
    exit()




dir = 0  # 0: 抬腿 1: 躺著
text = 'Leg Raises'
count = 0
accuracy = 0
accuracy_text = '開始動作'
displacement = 165
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Test_Media/Leg_raises.mp4')

        if not cap.isOpened():
            print("Cannot open camera")

            engine.say('Cannot open camera')
            engine.runAndWait()

            exit()

    detector = PoseDetector()

    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    accuracy = 0
    accuracy_text = '開始動作'
    displacement = 165
    angle_top1 = 180
    angle_top2 = 180
    while True:
        if(use_vedio or internal_test):
            success, img = cap.read()

        else:
            success = cap.read()[0]

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                angle = [landmarks[14], landmarks[12], landmarks[24],
                         landmarks[13], landmarks[11], landmarks[23],
                         landmarks[12], landmarks[24], landmarks[26],
                         landmarks[11], landmarks[23], landmarks[25],
                         landmarks[24], landmarks[26], landmarks[28],
                         landmarks[23], landmarks[25], landmarks[27],
                         landmarks[12], landmarks[14], landmarks[16],
                         landmarks[11], landmarks[13], landmarks[15],
                         landmarks[14], landmarks[15], landmarks[16],
                         landmarks[15], landmarks[14], landmarks[13]]
                
                angle = detector.findAngle(angle)

                #angle1:手肘到肩膀到寬的角度
                angle1_1 = angle[0]
                angle1_2 = angle[1]

                #angle2:肩膀到髖到膝蓋的角度
                angle2_1 = angle[2]
                angle2_2 = angle[3]

                #angle3:髖到膝蓋到腳踝的角度
                angle3_1 = angle[4]
                angle3_2 = angle[5]

                #angle4:肩膀到手肘到手腕的角度
                angle4_1 = angle[6]
                angle4_2 = angle[7]

                BREAK_1 = angle[8]
                BREAK_2 = angle[9]

                if 160 <= BREAK_1 + BREAK_2 <= 200:
                    break
                
                # 正確姿勢的範圍
                if 0 <= angle1_1 <= 32 and 0 <= angle1_2 <= 32 \
                    and 50 <= angle2_1 <= 180 and 50 <= angle2_2 <= 180 \
                    and 140 <= angle3_1 <= 178 and 140 <= angle3_2 <= 178 \
                    and 160 <= angle4_1 <= 180 and 160 <= angle4_2 <= 180:
                                    
                    # 目前狀態:抬腿
                    if dir == 0:   # 之前狀態:躺著
                        if 65 <= angle2_1 <= 90 and 65 <= angle2_2 <= 90:

                            # angle_top1:角度極值
                            if angle_top1 > (angle2_1 + angle2_2)/2:
                                angle_top1 = (angle2_1 + angle2_2)/2
                            # angle_top2:角度極值
                            if angle_top2 > (angle3_1 + angle3_2)/2:
                                angle_top2 = (angle3_1 + angle3_2)/2

                            count = count + 0.5
                            dir = 1    # 更新狀態:抬腿      

                    # 目前狀態:躺著
                    if dir == 1:# 之前狀態:抬腿
                        if 161 <= angle2_1 <= 180 and 161 <= angle2_2 <= 180:

                            accuracy1 = 100 - 2.5 * abs(angle_top1 - 80)    # 更新正確度
                            accuracy2 = 100 - 1.5 * abs(angle_top2 - 165)    # 更新正確度
                            accuracy = (accuracy1 + accuracy2) / 2
                            angle_top1 = 180
                            angle_top2 = 180
                            dir = 0    # 更新狀態:躺著

                            if(accuracy < 80):
                                count = count - 0.5
                                displacement = 220
                                if ( 65 <= angle_top1 < 72 and 140 <= angle_top2 < 152):
                                     accuracy_text = '腳不夠高 膝蓋太彎' 
                                elif ( 65 <= angle_top1 < 72):
                                     accuracy_text = '腳不夠高' 
                                elif ( 140 <= angle_top2 < 152):
                                     accuracy_text = '膝蓋太彎'

                            else:
                                count = count + 0.5
                                accuracy_text = str(int(accuracy)) + ' %'
                                displacement = 100
                            
                            if count % 1 == 0:
                                pygame.mixer.init()
                                pygame.mixer.music.load('./Test_Media/sound.wav')
                                pygame.mixer.music.play()

                else:
                    displacement = 165

                    if(count):
                        accuracy_text = '超出範圍'
                        print(angle1_1, angle1_2, angle2_1, angle2_2, angle3_1, angle3_2, angle4_1, angle4_2)

            img = Global_Use.sport(img, angle2_1, 90, 180, str(int(count)), accuracy_text, displacement, text, imgc, imgr)
            
            if(use_vedio or internal_test):
                cv2.imshow('Leg Raises', img)

            else:
                return dir, count, img, accuracy

        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#cap = 0
#Pose_Detected(cap, 1, dir , count, text, accuracy)
internal_test = 1
Pose_Detected(cap, 0, dir , count, text, accuracy)

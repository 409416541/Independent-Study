from PoseModule import PoseDetector
import Global_Use
import cv2
import pygame
import pyttsx3

cap = 0
dir = 0  # 0: 挺身 1: 伏地
text = 'Push Up'
count = 0
accuracy = 0
accuracy_text = '開始動作'
displacement = 165
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Test_Media/Push_up.mp4')
        
        if not cap.isOpened():
            print("Cannot open video")
            
            engine.say('Cannot open video')
            engine.runAndWait()

            exit()  

    if(internal_test):
        cap = cv2.VideoCapture(0)

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
    angle_top3 = 180
    angle1_1 = 0

    while True:
        if(use_vedio or internal_test):
            success, img = cap.read()

        else:
            success = cap.read()[0]

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                angle = [landmarks[11], landmarks[13], landmarks[15],
                         landmarks[12], landmarks[14], landmarks[16],
                         landmarks[11], landmarks[23], landmarks[25],
                         landmarks[12], landmarks[24], landmarks[26],
                         landmarks[23], landmarks[25], landmarks[27],
                         landmarks[24], landmarks[26], landmarks[28],
                         landmarks[14], landmarks[15], landmarks[16],
                         landmarks[15], landmarks[14], landmarks[13]]

                angle = detector.findAngle(angle)

                #angle1:肩膀到手肘到手腕的角度
                angle1_1 = angle[0]
                angle1_2 = angle[1]

                #angle2:肩膀到髖到膝蓋的角度
                angle2_1 = angle[2]
                angle2_2 = angle[3]

                #angle3:髖到膝蓋到腳踝
                angle3_1 = angle[4]
                angle3_2 = angle[5]
                
                break_1 = angle[6]
                break_2 = angle[7]

                if 160 <= break_1 + break_2 <= 200:
                    if(internal_test):
                        break

                    else:
                        return 100, count, img, accuracy
                
                # 正確姿勢的範圍
                if 140 <= angle2_1 <= 180 and 140 <= angle2_2 <= 180 \
                    and 140 <= angle3_1 <= 180 and 140 <= angle3_2 <= 180:

                    # 目前狀態:伏地
                    if dir == 0:   # 之前狀態:挺身
                        if 46 <= angle1_1 <= 95 and 46 <= angle1_2 <= 95:

                            # angle_top1:角度極值
                            if angle_top1 > (angle1_1 + angle1_2)/2:
                                angle_top1 = (angle1_1 + angle1_2)/2
                            if angle_top2 > (angle2_1 + angle2_2)/2:
                                angle_top2 = (angle2_1 + angle2_2)/2
                            if angle_top3 > (angle3_1 + angle3_2)/2:
                                angle_top3 = (angle3_1 + angle3_2)/2
                            count = count + 0.5
                            dir = 1    # 更新狀態:伏地

                    # 目前狀態:挺身
                    if dir == 1:   # 之前狀態:伏地
                        if 141 <= angle1_1 <= 180 and 141 <= angle1_2 <= 180:
                            accuracy1 = 100 - 1 * abs(angle_top1 - 60)    # 更新正確度
                            accuracy2 = 100 - 1 * abs(angle_top2 - 175)    # 更新正確度
                            accuracy3 = 100 - 1.2 * abs(angle_top3 - 170)    # 更新正確度
                            accuracy = (accuracy1 + accuracy2 + accuracy3) / 3
                            angle_top1 = 180
                            angle_top2 = 180
                            angle_top3 = 180
                            dir = 0    # 更新狀態:挺身
                            
                            if(accuracy < 80):
                                count = count - 0.5
                                displacement = 220
                                if ( 80 < angle_top1 <= 95 and 140 <= angle_top2 < 155 and 140 <= angle_top2 < 153):
                                     accuracy_text = '不夠下去 屁股太翹 膝蓋太彎' 
                                elif ( 80 < angle_top1 <= 95 and 140 <= angle_top2 < 155):
                                     accuracy_text = '不夠下去 屁股太翹' 
                                elif ( 80 < angle_top1 <= 95 and 140 <= angle_top2 < 153):
                                     accuracy_text = '不夠下去 膝蓋太彎' 
                                elif ( 140 <= angle_top2 < 155 and 140 <= angle_top2 < 153):
                                     accuracy_text = '屁股太翹 膝蓋太彎' 
                                elif ( 80 < angle_top1 <= 95):
                                     accuracy_text = '不夠下去' 
                                elif ( 140 <= angle_top2 < 155):
                                     accuracy_text = '屁股太翹'
                                elif ( 140 <= angle_top2 < 153):
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
                                    
            img = Global_Use.sport(img, angle1_1, 60, 175, str(int(count)), accuracy_text, displacement, text, imgc, imgr)
            
            if(use_vedio or internal_test):
                cv2.imshow('Push Up', img)

            else:
                return dir, count, img, accuracy
        
        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir , count, text, accuracy)
#internal_test = 1
#Pose_Detected(cap, 0, dir , count, text, accuracy)

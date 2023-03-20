from PoseModule import PoseDetector
import Global_Use
import cv2
import pygame
import pyttsx3

cap = 0
dir = 0  # 0: 開 1: 合
text = 'Jumping Jacks'
count = 0
accuracy = 0
accuracy_text = '開始動作'
displacement = 165
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Test_Media/Jumping_Jacks.mp4')

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
                         landmarks[26], landmarks[24], landmarks[23],
                         landmarks[25], landmarks[23], landmarks[24],
                         landmarks[16], landmarks[14], landmarks[12],
                         landmarks[15], landmarks[13], landmarks[11],
                         landmarks[26], landmarks[28], landmarks[27],
                         landmarks[25], landmarks[27], landmarks[28],
                         landmarks[14], landmarks[15], landmarks[16],
                         landmarks[15], landmarks[14], landmarks[13]]
                
                angle = detector.findAngle(angle)

                #手肘到肩膀到寬的角度
                angle1_1 = angle[0]
                angle1_2 = angle[1]

                #膝蓋到寬到寬的角度
                angle2_1 = angle[2]
                angle2_2 = angle[3]

                #手腕到手軸到肩膀的角度
                angle3_1 = angle[4]
                angle3_2 = angle[5]

                #膝蓋到腳踝到腳踝的角度
                angle4_1 = angle[6]
                angle4_2 = angle[7]

                break_1 = angle[8]
                break_2 = angle[9]

                if 160 <= break_1 + break_2 <= 200:
                    if(internal_test):
                        break

                    else:
                        return 100, count, img, accuracy

                if 0 <= angle1_1 <= 180 and  0 <= angle1_2 <= 180\
                    and 70 <= angle2_1 <= 125 and 70 <= angle2_2 <= 125\
                    and 50<=angle4_1 <= 110 and 50<=angle4_2 <= 110:
                        
                    # 目前狀態:開
                    if dir == 0: # 之前狀態:close
                        if 90 <= angle2_1 <= 125 and 150 <= angle1_1 <= 180\
                        and 90 <= angle2_2 <= 125 and 150 <= angle1_2 <= 180:
                            
                            if angle_top1 > (angle1_1 + angle1_2)/2:
                                angle_top1 = (angle1_1 + angle1_2)/2
                                
                            if angle_top2 > (angle2_1 + angle2_2)/2:
                                angle_top2 = (angle2_1 + angle2_2)/2

                            count = count + 0.5
                            dir = 1    # 更新狀態:關

                    # 目前狀態:關
                    if dir == 1: # 之前狀態:open
                        if 70 <= angle2_1 <= 90 and 0 <= angle1_1 <= 30\
                        and 170 <= angle3_1 <= 180 \
                        and 70 <= angle2_2 <= 90 and 0 <= angle1_2 <= 30\
                        and 170 <= angle3_2 <= 180:
                            
                            accuracy1 = 100 - 2.5 * abs(angle_top1 - 165)
                            accuracy2 = 100 - 1.5 * abs(angle_top2 - 115)
                            accuracy = (accuracy1+accuracy2)/2# 更新正確度
                            angle_top1 = 180
                            angle_top2 = 180
                            dir = 0    # 更新狀態:開

                            if(accuracy < 80):
                                count = count - 0.5
                                displacement = 220
                                print(angle1_1, angle1_2, angle2_1, angle2_2, angle3_1, angle3_2, angle4_1, angle4_2)
                                #最正確 angle1 = 165 angle2 = 115 
                                
                                if ( 150 <= angle_top1 < 157 and 90 <= angle_top2 < 102):
                                     accuracy_text = '手不夠高 腳不夠開' 
                                elif ( 173 < angle_top1 <= 180 and 90 <= angle_top2 < 102):
                                     accuracy_text = '手太高 腳不夠開' 
                                elif ( 150 <= angle_top1 < 157 ):
                                     accuracy_text = '手不夠高' 
                                elif ( 173 < angle_top1 <= 180 ):
                                     accuracy_text = '手太高'
                                elif ( 90 <= angle_top2 < 102 ):
                                     accuracy_text = '腳不夠開'
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

            img = Global_Use.sport(img, angle2_1, 80, 100, str(int(count)), accuracy_text, displacement, text, imgc, imgr)

            if(use_vedio or internal_test):
                cv2.imshow('Jumping Jacks', img)

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

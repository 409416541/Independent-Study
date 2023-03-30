from PoseModule import PoseDetector
import Global_Use
import cv2
import pygame
import pyttsx3

cap = 0
dir = 0  # 0: 仰臥 1: 起坐
text = 'Sit Ups'
count = 0
accuracy = 0
accuracy_count = 0
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy_count):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Test_Media/Sit_ups.mp4')

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
    displacement = 160
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
                angle = [landmarks[12], landmarks[24], landmarks[26],
                         landmarks[11], landmarks[23], landmarks[25],
                         landmarks[24], landmarks[26], landmarks[28],
                         landmarks[23], landmarks[25], landmarks[27],
                         landmarks[12], landmarks[14], landmarks[16],
                         landmarks[11], landmarks[13], landmarks[15],
                         landmarks[14], landmarks[15], landmarks[16],
                         landmarks[15], landmarks[14], landmarks[13]]
                
                angle = detector.findAngle(angle)

                #肩膀到髖到膝蓋
                angle1_1 = angle[0]
                angle1_2 = angle[1]

                #髖到膝蓋到腳踝
                angle2_1 = angle[2]
                angle2_2 = angle[3]

                #肩膀到手肘到手腕
                angle3_1 = angle[4]
                angle3_2 = angle[5]

                break_1 = angle[6]
                break_2 = angle[7]

                if 160 <= break_1 + break_2 <= 200 and landmarks[20][0] - landmarks[19][0] > 0:
                    if(internal_test):
                        break

                    else:
                        return 100, count, img, accuracy_count

                # 正確姿勢的範圍
                if 53 <= angle2_1 <= 110 and 53 <= angle2_2 <= 110 \
                    and 140 <= angle3_1 <= 177 and 140 <= angle3_2 <= 177 :

                    # 目前狀態:起坐
                    if dir == 0:  # 之前狀態:躺著
                        if 76 <= (angle1_1 + angle1_2)/2 <= 105:
                            
                            # angle_top1:角度極值
                            if angle_top1 > (angle1_1 + angle1_2)/2:
                                angle_top1 = (angle1_1 + angle1_2)/2
                            if angle_top2 > (angle2_1 + angle2_2)/2:
                                angle_top2 = (angle2_1 + angle2_2)/2
                            if angle_top3 > (angle3_1 + angle3_2)/2:
                                angle_top3 = (angle3_1 + angle3_2)/2
                            count = count + 0.5
                            dir = 1    # 更新狀態:起坐

                    # 目前狀態:躺著
                    if dir == 1:  # 之前狀態:起坐
                        if (angle1_1 + angle1_2)/2 >= 105:

                            accuracy1 = 100 - 2 * abs(angle_top1 - 85)
                            accuracy2 = 100 - 1.5 * abs(angle_top2 - 65)
                            accuracy3 = 100 - 1.5 * abs(angle_top3 - 165)
                            accuracy = (accuracy1 + accuracy2 + accuracy3)/3    # 更新正確度
                            accuracy_count += accuracy
                            angle_top1 = 180
                            angle_top2 = 180
                            angle_top3 = 180
                            dir = 0  # 更新狀態:躺著

                            if(accuracy < 65):
                                count = count - 0.5

                                if ( 95 < angle_top1 <= 105 and 78 < angle_top2 <= 90 and 140 <= angle_top3 <= 152):
                                     displacement = 195
                                     accuracy_text = '完全不符合' 
                                elif ( 95 < angle_top1 <= 105 and 78 < angle_top2 <= 90):
                                     displacement = 380
                                     accuracy_text = '腰不夠上來 膝蓋不夠彎' 
                                elif ( 95 < angle_top1 <= 105 and 140 <= angle_top3 <= 152):
                                     displacement = 345
                                     accuracy_text = '腰不夠上來 手軸太彎' 
                                elif (78 < angle_top2 <= 90 and 140 <= angle_top3 <= 152):
                                     displacement = 345
                                     accuracy_text = '膝蓋不夠彎 手軸太彎' 
                                elif ( 95 < angle_top1 <= 105):
                                     displacement = 195
                                     accuracy_text = '腰不夠上來'
                                elif ( 78 < angle_top2 <= 90):
                                     displacement = 195
                                     accuracy_text = '膝蓋不夠彎'
                                elif ( 140 <= angle_top3 <= 152):
                                     displacement = 160
                                     accuracy_text = '手軸太彎'

                            else:
                                count = count + 0.5
                                displacement = 100
                                accuracy_text = str(int(accuracy)) + ' %'                                
                            
                            if count % 1 == 0:
                                pygame.mixer.init()
                                pygame.mixer.music.load('./Test_Media/sound.wav')
                                pygame.mixer.music.play()

                else:
                    displacement = 160

                    if(count):
                        accuracy_text = '超出範圍'

            else:
                displacement = 160
                accuracy_text = '開始動作'
                                    
            img = Global_Use.sport(img, angle1_1, 85, 125, str(int(count)), accuracy_text, displacement, text, imgc, imgr)
            
            if(use_vedio or internal_test):
                cv2.imshow('Sit Ups', img)

            else:
                return dir, count, img, accuracy_count
                
        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir, count, text, accuracy_count)
#internal_test = 1
#Pose_Detected(cap, 0, dir, count, text, accuracy_count)

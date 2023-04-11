from PoseModule import PoseDetector
import Global_Use
import cv2
import pygame
import pyttsx3

cap = 0
dir = 0  # 0: 站起  1: 蹲下
text = 'Squat'
count = 0
accuracy = 0
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Test_Media/Squat.mp4')

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

    accuracy_text = '開始動作'
    displacement = 160
    angle_top1 = 180
    angle_top2 = 180
    angle1_1 = 0
    angle1_2 = 0

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
                         landmarks[14], landmarks[15], landmarks[16],
                         landmarks[15], landmarks[14], landmarks[13]]

                angle = detector.findAngle(angle)

                #angle1:肩膀到髖到膝蓋的角度
                angle1_1 = angle[0]
                angle1_2 = angle[1]

                #angle2:髖到膝蓋到腳踝的角度
                angle2_1 = angle[2]
                angle2_2 = angle[3]
                
                break_1 = angle[4]
                break_2 = angle[5]

                if 160 <= break_1 + break_2 <= 200\
                   and landmarks[16][0] - landmarks[15][0] > 10\
                   and landmarks[18][0] - landmarks[17][0] > 20\
                   and landmarks[20][0] - landmarks[19][0] > 20\
                   and landmarks[22][0] - landmarks[21][0] > 20:
                
                    if(internal_test):
                        break

                    else:
                        return 100, count, img, accuracy

                # 正確姿勢的範圍
                if 46 <= angle1_1 <= 180 and 46 <= angle1_2 <= 180 \
                    and 61 <= angle2_1 <= 180 and 61 <= angle2_2 <= 180:

                    # 目前狀態:蹲下
                    if dir == 0:  # 之前狀態:站起
                        if (46 <= angle1_1 <= 128 and 46 <= angle1_2 <= 128 \
                            and 61 <= angle2_1 <= 128 and 61 <= angle2_2 <= 128) or \
                            (((46 <= angle1_1 <= 128 and 61 <= angle2_1 <= 128) or \
                            (46 <= angle1_2 <= 128 and 61 <= angle2_2 <= 128)) and \
                            abs(angle1_1 - angle1_2)<25 and abs(angle2_1 - angle2_2)<35):

                            # angle_top1:角度極值
                            if angle_top1 > (angle1_1 + angle1_2)/2:
                                angle_top1 = (angle1_1 + angle1_2)/2
                            if angle_top2 > (angle2_1 + angle2_2)/2:
                                angle_top2 = (angle2_1 + angle2_2)/2    
                            count = count + 0.5
                            dir = 1    # 更新狀態:蹲下

                    # 目前狀態:站起
                    if dir == 1:  # 之前狀態:蹲下
                        if 141 <= angle1_1 <=180 and 141 <= angle1_2 <= 180 \
                            and 141 <= angle2_1 <= 180 and 141 <= angle2_2 <= 180:

                            accuracy1 = 100 - 0.6 * abs(angle_top1 - 65)
                            accuracy2 = 100 - 0.75 * abs(angle_top2 - 80)    
                            accuracy = (accuracy1 + accuracy2) / 2  # 更新正確度
                            angle_top1 = 180
                            angle_top2 = 180
                            dir = 0  # 更新狀態:站起

                            if(accuracy < 65):
                                count = count - 0.5
                                
                                if ( 88 < angle_top1 <= 128 and 107 < angle_top2 <= 128):
                                     displacement = 380
                                     accuracy_text = '蹲不夠下去 膝蓋不夠彎' 
                                elif ( 88 < angle_top1 <= 128):
                                     displacement = 195
                                     accuracy_text = '蹲不夠下去' 
                                elif ( 107 < angle_top2 <= 128):
                                     displacement = 195
                                     accuracy_text = '膝蓋不夠彎'

                            else:
                                count = count + 0.5
                                displacement = 100
                                accuracy_text = str(int(accuracy)) + ' %'
                            
                            if count % 1 == 0:
                                pygame.mixer.init()
                                pygame.mixer.music.load('./Test_Media/sound.wav')
                                pygame.mixer.music.play()

                elif (angle1_1 < 46 or angle1_1 > 180) and(angle1_2 < 46 or angle1_2 > 180) \
                    and (angle2_1 < 61 or angle2_1 > 180) and (angle2_2 < 61 or angle2_2 > 180):
                    displacement = 160

                    if(count):
                        accuracy_text = '超出範圍'

            else:
                displacement = 160
                accuracy_text = '開始動作'
                                
            img = Global_Use.sport(img, (angle1_1 + angle1_2)/2 - 10, 110, 175, str(int(count)), accuracy_text, displacement, text, imgc, imgr)
            
            if(use_vedio or internal_test):
                cv2.imshow('Squat', img)    

            else:
                return dir, count, img, accuracy
        
        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

Pose_Detected(cap, 1, dir, count, text, accuracy)
#internal_test = 1
#Pose_Detected(cap, 0, dir, count, text, accuracy_count)

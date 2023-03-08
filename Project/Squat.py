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
dir = 0  # 0: 站起  1: 蹲下
text = 'Squat'
count = 0
accuracy = 0
accuray_text = ''
displacement = 0
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Squat.mp4')

        if not cap.isOpened():
            print("Cannot open video")
            
            engine.say('Cannot open camera')
            engine.runAndWait()

            exit()  

    detector = PoseDetector()

    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    accuracy = 0
    accuray_text = ''
    displacement = 0
    angle_low = 180

    while True:
        if(use_vedio or internal_test):
            success, img = cap.read()

        else:
            success = cap.read()[0]

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            angle = [landmarks[12], landmarks[24], landmarks[26],
                     landmarks[11], landmarks[23], landmarks[25],
                     landmarks[24], landmarks[26], landmarks[28],
                     landmarks[23], landmarks[25], landmarks[27]]

            angle = detector.findAngle(angle)

            #angle1:肩膀到髖到膝蓋的角度
            angle1_1 = angle[0]
            angle1_2 = angle[1]

            #angle2:髖到膝蓋到腳踝的角度
            angle2_1 = angle[2]
            angle2_2 = angle[3]
            
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

                        # angle_low:角度極值
                        if angle_low > (angle1_1 + angle1_2)/2:
                            angle_low = (angle1_1 + angle1_2)/2

                        elif (angle1_1 + angle1_2)/2 - angle_low > 5:
                            count = count + 0.5
                            dir = 1    # 更新狀態:蹲下

                # 目前狀態:站起
                if dir == 1:  # 之前狀態:蹲下
                    if 141 <= angle1_1 <=180 and 141 <= angle1_2 <= 180 \
                        and 141 <= angle2_1 <= 180 and 141 <= angle2_2 <= 180:

                        accuracy = 100 - 0.75 * abs(angle_low - 65)    # 更新正確度
                        angle_low = 180
                        dir = 0   # 更新狀態:站起

                        if(accuracy < 58.75):
                            count = count - 0.5
                            accuray_text = 'Out of Range'
                            displacement = 220

                            if(angle1_1 < 70 and angle1_2 < 70):
                                accuray_text = '蹲太低'

                        else:
                            count = count + 0.5
                            accuray_text = str(int(accuracy)) + ' %'
                            displacement = 100
                        
                        if count % 1 == 0:
                            pygame.mixer.init()
                            pygame.mixer.music.load('./Project/Test_Media/sound.wav')
                            pygame.mixer.music.play()
                            #winsound.PlaySound("./Project/Test_Media/sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )

            img = Global_Use.sport(img, (angle1_1 + angle1_2)/2 - 10, 110, 175, str(int(count)), accuray_text, displacement, text, imgc, imgr)
            
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

#cap = 0
#Pose_Detected(cap, 1, dir , count, text, accuracy)
#internal_test = 1
#Pose_Detected(cap, 0, dir , count, text, accuracy)

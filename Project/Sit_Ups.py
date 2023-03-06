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
dir = 0  # 0: 仰臥 1: 起坐
count = 0
accuracy = 0
text_accuray = ''
displacement = 0
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Sit_ups.mp4')

        if not cap.isOpened():
            print("Cannot open video")
            
            engine.say('Cannot open camera')
            engine.runAndWait()

            exit()  

    detector = PoseDetector()

    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    accuracy = 0
    text_accuray = ''
    displacement = 0
    angle_top = 180

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

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

            # 正確姿勢的範圍
            if 50 <= angle2_1 <= 108 and 50 <= angle2_2 <= 108 \
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

                        if(accuracy < 58.75):
                            count = count - 1
                            text_accuray = 'Out of Range'
                            displacement = 220

                        else:
                            text_accuray = str(int(accuracy)) + ' %'
                            displacement = 120
                        
                        if count % 1 == 0:
                                pygame.mixer.init()
                                pygame.mixer.music.load('./Project/Test_Media/sound.wav')
                                pygame.mixer.music.play()
                                #winsound.PlaySound("./Project/Test_Media/sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )

            Global_Use.sport(img, angle1_1, 85, 125, str(int(count)), text_accuray, displacement, text, imgc, imgr)

            if(use_vedio or internal_test):
                cv2.imshow('Sit Ups', img)

            else:
                return dir, count, img, accuracy
        
        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir , count, 'Sit Ups', accuracy)
#internal_test = 1
#Pose_Detected(cap, 0, dir , count, 'Sit Ups', accuracy)

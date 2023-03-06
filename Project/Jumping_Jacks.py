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
dir = 0  # 0: 開 1: 合
count = 0
accuracy = 0
accuray_text = ''
displacement = 0
internal_test = 0

def Pose_Detected(cap, use_vedio, dir, count, text, accuracy):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Jumping_Jacks.mp4')

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
    angle_top1 = 180
    angle_top2 = 180

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            angle1_1, img = detector.findAngle(landmarks[14], landmarks[12],
                                            landmarks[24], img)
            angle1_2, img = detector.findAngle(landmarks[13], landmarks[11],
                                            landmarks[23], img)
            angle2_1, img = detector.findAngle(landmarks[26], landmarks[24],
                                            landmarks[23], img)
            angle2_2, img = detector.findAngle(landmarks[25], landmarks[23],
                                            landmarks[24], img)
            angle3_1, img = detector.findAngle(landmarks[16], landmarks[14],
                                            landmarks[12], img)
            angle3_2, img = detector.findAngle(landmarks[15], landmarks[13],
                                            landmarks[11], img)
            angle4_1, img = detector.findAngle(landmarks[26], landmarks[28],
                                            landmarks[27], img)
            angle4_2, img = detector.findAngle(landmarks[25], landmarks[27],
                                            landmarks[28], img)
            
            if 0 <= angle1_1 <= 180 and  0 <= angle1_2 <= 180\
                and 70 <= angle2_1 <= 125 and 70 <= angle2_2 <= 125\
                and 50<=angle4_1 <= 110 and 50<=angle4_2 <= 110:
                    
                # 目前狀態:合
                if dir == 0: # 之前狀態:open
                    if 90 <= angle2_1 <= 125 and 150 <= angle1_1 <= 180\
                    and 90 <= angle2_2 <= 125 and 150 <= angle1_2 <= 180:
                        
                        if angle_top1 > (angle1_1 + angle1_2)/2:
                            angle_top1 = (angle1_1 + angle1_2)/2
                            
                        if angle_top2 > (angle2_1 + angle2_2)/2:
                            angle_top2 = (angle2_1 + angle2_2)/2

                        count = count + 0.5
                        dir = 1    # 更新狀態:開

                # 目前狀態:開
                if dir == 1: # 之前狀態:close
                    if 70 <= angle2_1 <= 90 and 0 <= angle1_1 <= 30\
                    and 170 <= angle3_1 <= 180 \
                    and 70 <= angle2_2 <= 90 and 0 <= angle1_2 <= 30\
                    and 170 <= angle3_2 <= 180:
                        
                        accuracy1 = 100 - 1 * abs(angle_top1 - 165)
                        accuracy2 = 100 - 1 * abs(angle_top2 - 115)
                        accuracy = (accuracy1+accuracy2)/2# 更新正確度
                        angle_top1 = 180
                        angle_top2 = 180
                        dir = 0    # 更新狀態:合

                        if(accuracy < 60):
                            count = count - 0.5
                            accuray_text = 'Out of Range'
                            displacement = 220

                        else:
                            count = count + 0.5
                            accuray_text = str(int(accuracy)) + ' %'
                            displacement = 120
                        
                        if count % 1 == 0:
                            pygame.mixer.init()
                            pygame.mixer.music.load('./Project/Test_Media/sound.wav')
                            pygame.mixer.music.play()
                            #winsound.PlaySound("./Project/Test_Media/sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS ) 

            Global_Use.sport(img, angle2_1, 80, 100, str(int(count)), accuray_text, displacement, text, imgc, imgr)

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

#Pose_Detected(cap, 1, dir , count, 'Jumping Jacks', accuracy)
#internal_test = 1
#Pose_Detected(cap, 0, dir , count, 'Jumping Jacks', accuracy)

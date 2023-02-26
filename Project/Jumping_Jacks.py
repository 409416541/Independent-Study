from PoseModule import PoseDetector
import Global_Use
import cv2
import winsound
import pygame  
'''
cap = cv2.VideoCapture('./Project/Test_Media/Jumping_Jacks.mp4')

if not cap.isOpened():
    print("Cannot open video")
    exit()  



cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
'''

dir = 1  # 0: 開 1: 合
count = 0

def Pose_Detected(cap, use_vedio, dir, count, text):

    if(use_vedio):
        cap = cv2.VideoCapture('./Project/Test_Media/Jumping_Jacks.mp4')

        if not cap.isOpened():
            print("Cannot open video")
            exit()  

    detector = PoseDetector()
    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    accuracy1 = 0 
    accuracy2 = 0
    accuracy3 = 0
    accuracy4 = 0
    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
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
                
                # 顯示進度條
                Global_Use.thebar(img, angle2_1, 80, 100)
                
                if 0 <= angle1_1 <= 180 and  0 <= angle1_2 <= 180\
                    and 70 <= angle2_1 <= 125 and 70 <= angle2_2 <= 125\
                    and 50<=angle4_1 <= 110 and 50<=angle4_2 <= 110:
                        accuracy1=100
                        accuracy2=100
                        accuracy4=100
                        # 目前狀態::開
                        if dir==0: # 之前狀態:close
                            if 70 <= angle2_1 <= 90 and 0 <= angle1_1 <= 30\
                            and 170 <= angle3_1 <= 180 \
                            and 70 <= angle2_2 <= 90 and 0 <= angle1_2 <= 30\
                            and 170 <= angle3_2 <= 180:
                                count = count + 0.5
                                dir = 1    # 更新狀態:合
                                if count%1==0:
                                    pygame.mixer.init()
                                    pygame.mixer.music.load('./Project/Test_Media/sound.wav')
                                    pygame.mixer.music.play()
                                   #winsound.PlaySound("./Project/Test_Media/sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )

                                    
                        # 目前狀態::合
                        if dir==1: # 之前狀態:open

                            if 90 <= angle2_1 <= 125 and 150 <= angle1_1 <= 180\
                            \
                            and 90 <= angle2_2 <= 125 and 150 <= angle1_2 <= 180\
                            :
                                count = count + 0.5
                                dir = 0    # 更新狀態:開
                else:
                    if angle2_1<70:
                        accuracy2=100*(angle2_1/70)
                    if angle2_1>125:
                        accuracy2=100*(125/angle2_1)
                    if angle1_1>180:
                        accuracy1=100*(180/angle1_1)
                    if angle4_1<50:
                        accuracy4=100*(angle4_1/50) 
                    if angle4_1>110:
                        accuracy4=100*(110/angle4_1) 
                
                accuracy = ((accuracy1 +accuracy2+accuracy4) / 3)

                Global_Use.sport(img, str(int(count)), str(int(accuracy)) + ' %', text, imgc, imgr)

            if(not use_vedio):
                return dir, count, img

            else:
                cv2.imshow('Jumping Jacks', img)

        else:
            break

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir , count,'a')
#Pose_Detected(cap, 0, dir , count,'a')
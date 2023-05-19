from PoseModule import PoseDetector
import Global_Use
import cv2
import pygame

internal_test = 0
choose_count = 0

def Pose_Detected(cap, use_vedio, internal_test, choose_count):
    
    pygame.mixer.init()

    if(use_vedio):
        cap = cv2.VideoCapture('./data/Test_Media/Leg_raises.mp4')

        if not cap.isOpened():
            print("Cannot open video")
            
            pygame.mixer.music.load('./data/Voice//Cannot open video.wav')
            pygame.mixer.music.play()

            exit()  

    if(internal_test):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Cannot open camera")

            pygame.mixer.music.load('./data/Voice//Cannot open camera.wav')
            pygame.mixer.music.play()
                    
            exit()

    detector = PoseDetector()

    img = cap.read()[1]
    imgr, imgc = img.shape[:2]

    dir = 0  # 0: 抬腿 1: 躺著
    text = '仰臥抬腿'
    count = 0
    accuracy = 0
    accuracy_count = 0
    accuracy_text = '開始動作'
    displacement = 160
    angle_top1 = 180
    angle_top2 = 180
    angle2_1 = 0

    while True:
        success, img = cap.read()

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

                break_1 = angle[8]
                break_2 = angle[9]

                if 160 <= break_1 + break_2 <= 200\
                   and landmarks[16][0] - landmarks[15][0] > 10\
                   and landmarks[18][0] - landmarks[17][0] > 20\
                   and landmarks[20][0] - landmarks[19][0] > 20\
                   and landmarks[22][0] - landmarks[21][0] > 20\
                   or (count and count == choose_count):
                
                    if(internal_test):
                        break

                    else:
                        cv2.destroyAllWindows()

                        if(not count):
                            accuracy_count = 0

                        else:
                            accuracy_count = round(accuracy_count/count)

                        return 1, count, accuracy_count

                if 0 <= angle1_1 <= 32 and 0 <= angle1_2 <= 32 \
                    and 50 <= angle2_1 <= 180 and 50 <= angle2_2 <= 180 \
                    and 140 <= angle3_1 <= 178 and 140 <= angle3_2 <= 178 \
                    and 160 <= angle4_1 <= 180 and 160 <= angle4_2 <= 180:
                                    
                    if dir == 0:
                        if 65 <= angle2_1 <= 90 and 65 <= angle2_2 <= 90:

                            if angle_top1 > (angle2_1 + angle2_2)/2:
                                angle_top1 = (angle2_1 + angle2_2)/2

                            if angle_top2 > (angle3_1 + angle3_2)/2:
                                angle_top2 = (angle3_1 + angle3_2)/2

                            count = count + 0.5
                            dir = 1     

                    if dir == 1:
                        if 161 <= angle2_1 <= 180 and 161 <= angle2_2 <= 180:

                            accuracy1 = 100 - 2.5 * abs(angle_top1 - 80)   
                            accuracy2 = 100 - 1.5 * abs(angle_top2 - 165)
                            accuracy = (accuracy1 + accuracy2) / 2  # 更新正確度
                            angle_top1 = 180
                            angle_top2 = 180
                            dir = 0

                            if(accuracy < 75):
                                count = count - 0.5

                                if ( 65 <= angle_top1 < 72 and 140 <= angle_top2 < 152):
                                     displacement = 310
                                     accuracy_text = '腳不夠高 膝蓋太彎' 
                                elif ( 65 <= angle_top1 < 72):
                                     displacement = 160
                                     accuracy_text = '腳不夠高' 
                                elif ( 140 <= angle_top2 < 152):
                                     displacement = 160
                                     accuracy_text = '膝蓋太彎'

                            else:
                                count = count + 0.5
                                displacement = 100
                                accuracy_text = str(int(accuracy)) + ' %'
                                accuracy_count += accuracy      
                            
                            if count % 1 == 0:
                                pygame.mixer.init()
                                pygame.mixer.music.load('./data/Voice/sound.wav')
                                pygame.mixer.music.play()

                elif (angle1_1<0 or angle1_1 >32) and (angle1_2<0 or angle1_2 >32) \
                    and (angle2_1<50 or angle2_1 >180) and (angle2_2<50 or angle2_2 >180)\
                    and (angle3_1<140 or angle3_1 >178) and(angle3_2<140 or angle3_2 >178) \
                    and (angle4_1<160 or angle4_1 > 180) and (angle4_2<160 or angle4_2 > 180):
                    displacement = 160

                    if(count):
                        accuracy_text = '超出範圍'

            else:
                displacement = 160
                accuracy_text = '開始動作'

            img = Global_Use.sport(img, angle2_1, 90, 180, str(int(count)), accuracy_text, displacement, text, imgc, imgr)
            
            cv2.imshow(text, img)

        else:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir, count, text, accuracy_count)
#internal_test = 1
#Pose_Detected(cap, 0, dir, count, text, accuracy_count)

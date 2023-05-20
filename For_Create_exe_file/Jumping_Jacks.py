from PoseModule import PoseDetector
import Global_Use
import cv2
import pygame

internal_test = 0
choose_count = 0

def Pose_Detected(cap, use_vedio, internal_test, choose_count):
    
    pygame.mixer.init()

    if(use_vedio):
        cap = cv2.VideoCapture('./data/Test_Media/Jumping_Jacks.mp4')

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

    dir = 0 # 0: 開 1: 合
    text = '開合跳'
    text_en = 'Jumping Jacks'
    bar_displacement = 0
    count = 0
    accuracy = 0
    accuracy_count = 0
    accuracy_text = '開始動作'
    text_displacement = 160
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

                if 0 <= angle1_1 <= 180 and  0 <= angle1_2 <= 180\
                    and 70 <= angle2_1 <= 125 and 70 <= angle2_2 <= 125\
                    and 50<=angle4_1 <= 110 and 50<=angle4_2 <= 110:
                        
                    if dir == 0:
                        if 90 <= angle2_1 <= 125 and 150 <= angle1_1 <= 180\
                        and 90 <= angle2_2 <= 125 and 150 <= angle1_2 <= 180:
                            
                            if angle_top1 > (angle1_1 + angle1_2)/2:
                                angle_top1 = (angle1_1 + angle1_2)/2
                                
                            if angle_top2 > (angle2_1 + angle2_2)/2:
                                angle_top2 = (angle2_1 + angle2_2)/2

                            count = count + 0.5
                            dir = 1

                    if dir == 1:
                        if 70 <= angle2_1 <= 90 and 0 <= angle1_1 <= 30\
                        and 170 <= angle3_1 <= 180 \
                        and 70 <= angle2_2 <= 90 and 0 <= angle1_2 <= 30\
                        and 170 <= angle3_2 <= 180:
                            
                            accuracy1 = 100 - 2.5 * abs(angle_top1 - 160)
                            accuracy2 = 100 - 1.5 * abs(angle_top2 - 115)
                            accuracy = (accuracy1+accuracy2)/2  # 更新正確度
                            angle_top1 = 180
                            angle_top2 = 180
                            dir = 0

                            if(accuracy < 75):
                                count = count - 0.5
                                
                                if ( 150 <= angle_top1 < 157 and 90 <= angle_top2 < 102):
                                     text_displacement = 310
                                     accuracy_text = '手不夠高 腳不夠開' 
                                elif ( 173 < angle_top1 <= 180 and 90 <= angle_top2 < 102):
                                     text_displacement = 275
                                     accuracy_text = '手太高 腳不夠開' 
                                elif ( 150 <= angle_top1 < 157 ):
                                     text_displacement = 160
                                     accuracy_text = '手不夠高' 
                                elif ( 173 < angle_top1 <= 180 ):
                                     text_displacement = 125
                                     accuracy_text = '手太高'
                                elif ( 90 <= angle_top2 < 102 ):
                                     text_displacement = 160
                                     accuracy_text = '腳不夠開'

                            else:
                                count = count + 0.5
                                text_displacement = 100
                                accuracy_text = str(int(accuracy)) + ' %'
                                accuracy_count += accuracy
                            
                            if count % 1 == 0:
                                pygame.mixer.init()
                                pygame.mixer.music.load('./data/Voice/sound.wav')
                                pygame.mixer.music.play()

                
                elif angle1_1 > 180 and  angle1_2 > 180\
                    and (angle2_1< 70 or angle2_1 > 125) and (angle2_2 < 70 or angle2_2) > 125\
                    and (angle4_1 < 50 or angle4_1 > 110) and (angle4_2 < 50 or angle4_2) > 110:
                        
                    text_displacement = 160

                    if(count):
                        accuracy_text = '超出範圍'

            else:
                text_displacement = 160
                accuracy_text = '開始動作'

            if(count >= 10):
                bar_displacement = 40
               
            img = Global_Use.sport(img, angle2_1, 80, 100, bar_displacement, str(int(count)), accuracy_text, text_displacement, text, imgc, imgr)

            cv2.imshow(text_en, img)
            
        else:
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected(cap, 1, dir, count, text, accuracy)
#internal_test = 1
#Pose_Detected(cap, 0, dir, count, text, accuracy)

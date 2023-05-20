import Global_Use
import cv2
import mediapipe as mp
import math
import numpy as np

mp_hands = mp.solutions.hands

def findAngle(p1,p2, p3):

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))

    if angle < 0:
        angle += 360
            
    if angle > 180:
        angle = 360 - angle

    return angle

def hand_angle(hand_):

    angle_list = []

    # 1 表示手指伸直，0 表示手指捲縮

    # thumb 大拇指
    if(findAngle(hand_[4], hand_[3], hand_[2]) >= 150 and findAngle(hand_[3], hand_[2], hand_[1]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)

    # index 食指
    if(findAngle(hand_[8], hand_[7], hand_[6]) >= 160 and findAngle(hand_[7], hand_[6], hand_[5]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)

    # middle 中指
    if(findAngle(hand_[12], hand_[11], hand_[10]) >= 160 and findAngle(hand_[11], hand_[10], hand_[9]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)

    # ring 無名指
    if(findAngle(hand_[16], hand_[15], hand_[14]) >= 160 and findAngle(hand_[15], hand_[14], hand_[13]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)

    # pinky 小拇指
    if(findAngle(hand_[20], hand_[19], hand_[18]) >= 160 and findAngle(hand_[19], hand_[18], hand_[17]) >= 148):
        angle_list.append(1)
    else:
        angle_list.append(0)

    return angle_list

def hand_pos(finger_angle):

    match finger_angle:
        case [0, 0, 0, 0, 0]:
            return '0'
        case [0, 1, 0, 0, 0]:
            return '1'
        case [0, 1, 1, 0, 0]:
            return '2'
        case [0, 1, 1, 1, 0]:
            return '3'
        case [0, 1, 1, 1, 1]:
            return '4'
        case [1, 1, 1, 1, 1]:
            return '5'
        case [1, 0, 0, 0, 1]:
            return '6'
        case _:
            return 'NAN'

'''
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Cannot open camera')
    exit()
'''

# mediapipe 啟用偵測手掌
def Hand_Detecter(cap):

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        w, h = 540, 310                                  # 影像尺寸
        last_test = ''

        while True:
            img = cap.read()[1]

            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
            results = hands.process(img2)                # 偵測手勢

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    finger_points = []                   # 記錄手指節點座標的串列

                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x * w
                        y = i.y * h
                        finger_points.append((x, y))

                    if finger_points:
                        finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                        #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                        text = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                        
                        if(last_test != text):
                            last_test = text
                        #Global_Use.thecount(img, text)
                        
            background = img.copy()
            background[:, :, :] = 0 
            
            return background, last_test

            '''
            cv2.imshow('Hand Detecter', img)
            if cv2.waitKey(5) == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
    '''
    
#Hand_Detecter(cap)

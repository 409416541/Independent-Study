import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# 根據兩點的座標，計算角度
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

# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []

    # thumb 大拇指角度
    if(findAngle(hand_[4], hand_[3], hand_[2]) >= 160 and findAngle(hand_[3], hand_[2], hand_[1]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)
    print(findAngle(hand_[3], hand_[2], hand_[1]))
    # index 食指角度
    if(findAngle(hand_[8], hand_[7], hand_[6]) >= 160 and findAngle(hand_[7], hand_[6], hand_[5]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)

    # middle 中指角度
    if(findAngle(hand_[12], hand_[11], hand_[10]) >= 160 and findAngle(hand_[11], hand_[10], hand_[9]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)

    # ring 無名指角度
    if(findAngle(hand_[16], hand_[15], hand_[14]) >= 160 and findAngle(hand_[15], hand_[14], hand_[13]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)

    # pink 小拇指角度
    if(findAngle(hand_[20], hand_[19], hand_[18]) >= 160 and findAngle(hand_[19], hand_[18], hand_[17]) >= 160):
        angle_list.append(1)
    else:
        angle_list.append(0)

    return angle_list

# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 1 表示手指伸直，0 表示手指捲縮
    if f1 == 0 and f2 == 1 and f3 == 0 and f4 == 0 and f5 == 0:
        return '1'
    elif f1 == 0 and f2 == 1 and f3 == 1 and f4 == 0 and f5 == 0:
        return '2'
    elif f1 == 0 and f2 == 1 and f3 == 1 and f4 == 1 and f5 == 0:
        return '3'
    elif f1 == 0 and f2 == 1 and f3 == 1 and f4 == 1 and f5 == 1:
        return '4'
    elif f1 == 1 and f2 == 1 and f3 == 1 and f4 == 1 and f5 == 1:
        return '5'
    elif f1 == 1 and f2 == 0 and f3 == 0 and f4 == 0 and f5 == 0:
        return 'good'
    elif f1 == 0 and f2 == 0 and f3 == 1 and f4 == 0 and f5 == 0:
        return 'no!!!'
    else:
        return ''

cap = cv2.VideoCapture(0)            # 讀取攝影機
fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
lineType = cv2.LINE_AA               # 印出文字的邊框

# mediapipe 啟用偵測手掌
def Hand_Detecter():
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        w, h = 540, 310                                  # 影像尺寸
        while True:
            ret, img = cap.read()

            if not ret:
                print("Cannot receive frame")
                break
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
            results = hands.process(img2)                # 偵測手勢
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    finger_points = []                   # 記錄手指節點座標的串列
                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x*w
                        y = i.y*h
                        finger_points.append((x,y))
                    if finger_points:
                        finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                        #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                        text = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                        cv2.putText(img, text, (30,120), fontFace, 5, (255,255,255), 10, lineType) # 印出文字

            cv2.imshow('oxxostudio', img)
            if cv2.waitKey(5) == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

Hand_Detecter()
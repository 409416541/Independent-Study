from Hand_Detecter import Hand_Detecter as hd
from Sit_Ups import Pose_Detected as pose1
from Push_Up import Pose_Detected as pose2
from Squat import Pose_Detected as pose3
from Leg_Raises import Pose_Detected as pose4
from Jumping_Jacks import Pose_Detected as pose5
import Global_Use
import cv2
import time

cap = cv2.VideoCapture(0)
if not cap.isOpened():
            print("Cannot open camera")
            exit()

confirm = 0
has_choose = 0
last_choose = ''
bye = 0
count = 3

text = ['Please choose action', 
        '1. Sit Ups', '2. Push Up', '3. Squat', '4. Leg Raises', '5. Jumping Jacks', '6. Break',
        'Your choose is ', 'Rock. OK', 'Fuck. NO']

while(count+1 >= 0):
    if(not confirm):
        img, choose = hd(cap)

        if(not has_choose):
            Global_Use.interface(img, text[0], 30)
            Global_Use.interface(img, text[1], 65)
            Global_Use.interface(img, text[2], 105)
            Global_Use.interface(img, text[3], 145)
            Global_Use.interface(img, text[4], 180)
            Global_Use.interface(img, text[5], 215)
            Global_Use.interface(img, text[6], 250)

            if(choose == '1' or choose == '2' or choose == '3' or choose == '4' or choose == '5' or choose == '6'):
                has_choose = 1
                last_choose = choose

        else:
            Global_Use.confirm(img, text[7] + text[int(last_choose)], 30)
            Global_Use.confirm(img, text[8], 65)
            Global_Use.confirm(img, text[9], 105)

            if(choose == 'NO'):
                has_choose = 0
                continue

            elif(choose == 'OK'):
                confirm = 1

                if(last_choose == '6'):
                    bye = 1

    elif(not bye):
        match last_choose:
            case '1':
                img = pose1(cap)
            case '2':
                img = pose2(cap)
            case '3':
                img = pose3(cap)
            case '4':
                img = pose4(cap)
            case '5':
                img = pose5(cap)
        
    if(bye):
        img = cap.read()[1]
        x, y = img.shape[:2]

        if(count > 0):
            Global_Use.byebyecount(img, str(count), x, y)

        else:
            Global_Use.byebyecount(img, 'Bye', x//3 + 4, y)

        count -= 1
        time.sleep(1)

    cv2.imshow('POSE', img)

    if cv2.waitKey(5) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
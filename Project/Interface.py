from Hand_Detecter import Hand_Detecter as hd
from Sit_Ups import Pose_Detected as pose1
from Push_Up import Pose_Detected as pose2
from Squat import Pose_Detected as pose3
from Leg_Raises import Pose_Detected as pose4
from Jumping_Jacks import Pose_Detected as pose5
import Global_Use
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
            print("Cannot open camera")
            exit()

last_choose = ''
has_choose = 0
confirm = 0

while 1:
    img, choose = hd(cap)

    text = ['Please choose action', '1. Sit Ups', '2. Push Up', '3. Squat', '4. Leg Raises', '5. Jumping Jacks',
            'Your choose is ', 'Rock. OK', 'Fuck. NO']

    if(not has_choose):
        cv2.putText(img, text[0], (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))
        cv2.putText(img, text[1], (10, 65), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))
        cv2.putText(img, text[2], (10, 105), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))
        cv2.putText(img, text[3], (10, 145), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))
        cv2.putText(img, text[4], (10, 180), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))
        cv2.putText(img, text[5], (10, 215), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))

        if(choose == '1' or choose == '2' or choose == '3' or choose == '4' or choose == '5'):
            has_choose = 1
            last_choose = choose

    elif(not confirm):
        cv2.putText(img, text[6] + last_choose, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 92, 186), 2)
        cv2.putText(img, text[7], (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 92, 186), 2)
        cv2.putText(img, text[8], (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 92, 186), 2)

        if(choose == 'YES'):
            confirm = 1

        elif(choose == 'NO'):
            has_choose = 0

    else:
        cv2.putText(img, 'haaaaaaaaaaa', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))
        
        

    cv2.imshow('POSE', img)

    
    if cv2.waitKey(5) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
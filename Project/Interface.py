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

count = 3 # break 時的倒數
bye = 0 # 若為1則表使用者要退出
confirm = 0 # 若為1則表使用者已確認所選動作無誤
has_choose = 0 # 若為1則表使用者以選擇動作
last_choose = '' # 紀錄下剛剛讀取的動作選擇為何
vedio_confirm = 0 # 若為1則表使用則所選擇的影片無誤
vedio_has_choose = 0 # 若為1表使用者已選擇要看範例影片或做運動
last_vedio_choose = '' # 紀錄下剛剛讀取的影片選擇為何
count_times_confirm = 0 # 若為1則表使用者以確認動作要做幾下
count_times_choose = 0 # 若為1則表使用者以選擇動作要做幾下
at_choose_times = '' # 紀錄下剛剛讀取的次數選擇為何
choose_times = '' # 紀錄下剛剛讀取的次數選擇為何(不含 '4. back to choose')
count_times= 0 # 紀錄目前使用者以做幾下了

difficulty = [8, 15, 25]

text = ['Please choose action', 
        '1. Sit Ups', '2. Push Up', '3. Squat', '4. Leg Raises', '5. Jumping Jacks', '6. Break', # interface
        'Your choose is ', 
        'Rock. OK', 'Pink. NO',
        'Please choose you want', 
        '1. Sample Video', '2. Go Sport', '3. back to interface',
        'How times you want', 
        '1.  '+str(difficulty[0])+' times', '2. '+str(difficulty[1])+' times', '3. '+str(difficulty[2])+' times', '4. back to choose'] 

while(count+1 >= 0):

    if(bye):
        img = cap.read()[1]
        x, y = img.shape[:2]

        if(count > 0):
            Global_Use.byebyecount(img, str(count), x, y)

        else:
            Global_Use.byebyecount(img, 'Bye', x//3 + 4, y)

        count -= 1
        time.sleep(1)

    elif(not confirm):
        img, choose = hd(cap)

        if(not has_choose):
             # interface
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

            elif(choose == 'OK'):
                confirm = 1

                if(last_choose == '6'):
                    bye = 1

    else:
        img, choose = hd(cap)

        if(not vedio_confirm):

            if(not vedio_has_choose):
                # choose
                Global_Use.interface(img, text[10], 30)
                Global_Use.interface(img, text[11], 65)
                Global_Use.interface(img, text[12], 105)
                Global_Use.interface(img, text[13], 145)

                if(choose == '1' or choose == '2' or choose == '3'):
                    vedio_has_choose = 1
                    last_vedio_choose = choose

            else:
                Global_Use.confirm(img, text[7] + text[int(last_vedio_choose) + 10], 30)
                Global_Use.confirm(img, text[8], 65)
                Global_Use.confirm(img, text[9], 105)

                if(choose == 'NO'):
                        vedio_has_choose = 0

                elif(choose == 'OK'):

                    if(last_vedio_choose == '3'):
                        confirm = 0
                        has_choose = 0
                        vedio_confirm = 0
                        vedio_has_choose = 0

                    else:
                        vedio_confirm = 1

        else:
            if(last_vedio_choose == '1'):
                match last_choose:
                    case '1':
                        pose1(cap, 1)
                    case '2':
                        pose2(cap, 1)
                    case '3': 
                        pose3(cap, 1)
                    case '4':
                        pose4(cap, 1)
                    case '5':
                        pose5(cap, 1)
                
                vedio_confirm = 0
                vedio_has_choose = 0

            elif(last_vedio_choose == '2'):
                if(not count_times_confirm):

                    if(not count_times_choose):
                        Global_Use.interface(img, text[14], 30)
                        Global_Use.interface(img, text[15], 65)
                        Global_Use.interface(img, text[16], 105)            
                        Global_Use.interface(img, text[17], 145)
                        Global_Use.interface(img, text[18], 180)

                        if(choose == '1' or choose == '2' or choose == '3' or choose == '4'):
                            count_times_choose = 1
                            at_choose_times = choose

                            if(choose != '4'):
                                choose_times = choose

                    else:
                        Global_Use.confirm(img, text[7] + text[int(at_choose_times) + 14], 30)
                        Global_Use.confirm(img, text[8], 65)
                        Global_Use.confirm(img, text[9], 105)

                        if(choose == 'NO'):
                            count_times_choose = 0

                        elif(choose == 'OK'):

                            if(at_choose_times == '4'):
                                vedio_confirm = 0
                                vedio_has_choose = 0
                                count_times_confirm = 0
                                count_times_choose = 0


                            else:
                                count_times_confirm = 1

                else:
                    match last_choose:
                        case '1':
                            count_times, img = pose1(cap, 0)
                        case '2':
                            count_times, img = pose2(cap, 0)
                        case '3':
                            count_times, img = pose3(cap, 0)
                        case '4':
                            count_times, img = pose4(cap, 0)
                        case '5':
                            count_times, img = pose5(cap, 0)

                    if(count_times == difficulty[int(choose_times) - 1]):
                        confirm = 0
                        has_choose = 0
                        vedio_confirm = 0
                        vedio_has_choose = 0
                        count_times_confirm = 0
                        count_times_choose = 0

    cv2.imshow('POSE', img)

    if cv2.waitKey(5) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
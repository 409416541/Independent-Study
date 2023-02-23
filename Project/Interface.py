from Hand_Detecter import Hand_Detecter as hd
from Sit_Ups import Pose_Detected as pose1
from Push_Up import Pose_Detected as pose2
from Squat import Pose_Detected as pose3
from Leg_Raises import Pose_Detected as pose4
from Jumping_Jacks import Pose_Detected as pose5
import Global_Use
import cv2
import numpy as np
import time
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
            print('Cannot open camera')
            engine.say('Cannot open camera')
            engine.runAndWait()

            exit()

img = cap.read()[1]
imgr, imgc = img.shape[:2]

start = 0.0
end = 0.0
wait_time = 0.3

nan_start = 0.0
nan_end = 0.0

other_start = 0.0
other_end = 0.0
other_time = 0.1

count = 3 # break 時的倒數
bye = 0 # 若為1則表使用者要退出
confirm = 0 # 若為1則表使用者已確認所選動作無誤
has_choose = 0 # 若為1則表使用者以選擇動作
last_choose = 'NAN' # 紀錄下剛剛讀取的動作選擇為何
vedio_confirm = 0 # 若為1則表使用則所選擇的影片無誤
vedio_has_choose = 0 # 若為1表使用者已選擇要看範例影片或做運動
last_vedio_choose = 'NAN' # 紀錄下剛剛讀取的影片選擇為何
count_times_confirm = 0 # 若為1則表使用者以確認動作要做幾下
count_times_choose = 0 # 若為1則表使用者以選擇動作要做幾下
last_times_choose = 'NAN' # 紀錄下剛剛讀取的次數選擇為何
dir = 0
count_times= 0.0 # 紀錄目前使用者以做幾下了

difficulty = [8, 15, 25]

text = ['Please choose action', 
        '1. Sit Ups', '2. Push Up', '3. Squat', '4. Leg Raises', '5. Jumping Jacks', '6. Break', # interface
        'Your choose is ', 
        'Please choose you want', 
        '1. Sample Video', '2. Go Sport', '3. back to interface', # choose
        'How times you want', 
        '1.  '+str(difficulty[0])+' times', '2. '+str(difficulty[1])+' times', '3. '+str(difficulty[2])+' times', '4. back to choose'] 

choose_text = ['Bye',
               'Sit Up', 'Push Up', 'Squat', 'Leg Raises', 'Jumping Jacks', 'Break',
               'Sample Video', 'Go Sport', 'back to interface',
               str(difficulty[0])+' times', str(difficulty[1])+' times', str(difficulty[2])+' times', 'back to choose']

while(count+1 >= 0):

    if(bye):
        img[:, :, :] = 255

        if(count > 0):
            Global_Use.byebyecount(img, str(count), imgr, imgc)

        else:
            Global_Use.byebyecount(img, 'Bye', imgr//3 + 4, imgc)

        count -= 1
        time.sleep(1)

    elif(not confirm):
        img, choose = hd(cap)

        # interface
        Global_Use.interface(img, text[0], 30)
        Global_Use.interface(img, text[1], 75)
        Global_Use.interface(img, text[2], 110)
        Global_Use.interface(img, text[3], 145)
        Global_Use.interface(img, text[4], 180)
        Global_Use.interface(img, text[5], 215)
        Global_Use.interface(img, text[6], 250)

        Global_Use.handpose(img, choose, imgr, imgc)

        if(not has_choose):
            if(choose == '1' or choose == '2' or choose == '3' or choose == '4' or choose == '5' or choose == '6'):
                has_choose = 1
                last_choose = choose
                start = time.time()

        else:
            if(choose == last_choose or choose == '0'):
                nan_start = 0.0
                end = time.time()
                other_start = 0.0

                if(start and end - start > wait_time and choose == '0'):
                    confirm = 1
                    start = 0.0
                    end = 0.0
                    nan_start = 0.0
                    nan_end = 0.0
                    other_start = 0.0
                    other_end = 0.0

                    engine.say(choose_text[int(last_choose)])
                    engine.runAndWait()

                    if(last_choose == '6' and choose == '0'):
                        bye = 1

            elif(not nan_start and choose == 'NAN'):
                has_choose = 1
                nan_start = time.time()

            elif(nan_start):
                nan_end = time.time()

                if(nan_end - nan_start > wait_time):
                    has_choose = 0
                    end = 0.0
                    nan_end = 0.0

            elif(other_end - other_start > other_time):
                has_choose = 0
                end = 0.0
                other_start = 0.0
                other_end = 0.0
                    
            elif(not other_start):
                other_start = time.time()

            elif(other_start):
                    other_end = time.time()

    else:
        img, choose = hd(cap)

        if(not vedio_confirm):
            if(choose == '4' or choose == '5' or choose == '6'):
                choose = 'NAN'

            # choose
            Global_Use.interface(img, text[7] + text[int(last_choose)], 30)
            Global_Use.interface(img, text[8], 65)
            Global_Use.interface(img, text[9], 110)
            Global_Use.interface(img, text[10], 145)
            Global_Use.interface(img, text[11], 180)

            Global_Use.handpose(img, choose, imgr, imgc)

            if(not vedio_has_choose):
                if(choose == '1' or choose == '2' or choose == '3'):
                    vedio_has_choose = 1
                    last_vedio_choose = choose
                    start = time.time()

            else:
                if(not nan_start and choose == 'NAN'):
                    vedio_has_choose = 1
                    nan_start = time.time()

                elif(nan_start):
                    nan_end = time.time()

                    if(nan_end - nan_start > wait_time):
                        vedio_has_choose = 0
                        end = 0.0
                        nan_end = 0.0

                elif(other_end - other_start > other_time):
                    vedio_has_choose = 0
                    end = 0.0
                    other_start = 0.0
                    other_end = 0.0

                elif(not other_start):
                    other_start = time.time()

                elif(other_start):
                    other_end = time.time()

                if(choose == last_vedio_choose or choose == '0'):
                    nan_start = 0.0
                    end = time.time()

                    if(start and end - start > wait_time and choose == '0'):
                        vedio_confirm = 1
                        start = 0.0
                        end = 0.0
                        nan_start = 0.0
                        nan_end = 0.0
                        other_start = 0.0
                        other_end = 0.0

                        engine.say(choose_text[int(last_vedio_choose)+6])
                        engine.runAndWait()

        else:
            match last_vedio_choose:

                case '1':
                    match last_choose:

                        case '1':
                            pose1(cap, 1, 0, 0.0, '')
                        case '2':
                            pose2(cap, 1, 0, 0.0, '')
                        case '3': 
                            pose3(cap, 1, 0, 0.0, '')
                        case '4':
                            pose4(cap, 1, 0, 0.0, '')
                        case '5':
                            pose5(cap, 1, 0, 0.0, '')
                    
                    vedio_confirm = 0
                    vedio_has_choose = 0

                case '2':
                    if(not count_times_confirm):
                        if(choose == '4' or choose == '5' or choose == '6'):
                            choose = 'NAN'

                        Global_Use.interface(img, text[12], 30)
                        Global_Use.interface(img, text[13], 75)
                        Global_Use.interface(img, text[14], 110)            
                        Global_Use.interface(img, text[15], 145)
                        Global_Use.interface(img, text[16], 180)

                        Global_Use.handpose(img, choose, imgr, imgc)

                        if(not count_times_choose):
                            if(choose == '1' or choose == '2' or choose == '3' or choose == '4'):
                                count_times_choose = 1
                                last_times_choose = choose
                                start = time.time()

                        else:
                            if(choose == last_times_choose or choose == '0'):
                                nan_start = 0.0
                                end = time.time()

                                if(start and end - start > wait_time and choose == '0'):
                                    if(last_times_choose == '4'):
                                        vedio_confirm = 0
                                        vedio_has_choose = 0
                                        count_times_confirm = 0
                                        count_times_choose = 0
                                        start = 0.0
                                        end = 0.0
                                        nan_start = 0.0
                                        nan_end = 0.0
                                        other_start = 0.0
                                        other_end = 0.0

                                    else:
                                        count_times_confirm = 1
                                        start = 0.0
                                        end = 0.0
                                        nan_start = 0.0
                                        nan_end = 0.0
                                        other_start = 0.0
                                        other_end = 0.0

                                        engine.say(choose_text[int(last_times_choose)+9])
                                        engine.runAndWait()

                            elif(not nan_start and choose == 'NAN'):
                                count_times_choose = 1
                                nan_start = time.time()

                            elif(nan_start):
                                nan_end = time.time()

                                if(nan_end - nan_start > wait_time):
                                    count_times_choose = 0
                                    end = 0.0

                            elif(other_end - other_start > other_time):
                                count_times_choose = 0
                                end = 0.0
                                other_start = 0.0
                                other_end = 0.0
                                    
                            elif(not other_start):
                                other_start = time.time()

                            elif(other_start):
                                other_end = time.time()

                    else:
                        match last_choose:
                            
                            case '1':
                                dir, count_times, img = pose1(cap, 0, dir, count_times, text[int(last_choose)])
                            case '2':
                                dir, count_times, img = pose2(cap, 0, dir, count_times, text[int(last_choose)])
                            case '3':
                                dir, count_times, img = pose3(cap, 0, dir, count_times, text[int(last_choose)])
                            case '4':
                                dir, count_times, img = pose4(cap, 0, dir, count_times, text[int(last_choose)])
                            case '5':
                                dir, count_times, img = pose5(cap, 0, dir, count_times, text[int(last_choose)])

                        if(count_times == difficulty[int(last_times_choose) - 1]):
                            confirm = 0
                            has_choose = 0
                            vedio_confirm = 0
                            vedio_has_choose = 0
                            count_times_confirm = 0
                            count_times_choose = 0
                            count_times = 0.0

                            other_start = 0.0
                            other_end = 0.0

                case '3':
                    confirm = 0
                    has_choose = 0
                    vedio_confirm = 0
                    vedio_has_choose = 0
                    other_start = 0.0
                    other_end = 0.0

    cv2.imshow('POSE', img)

    if cv2.waitKey(5) == ord('q'):
        break

engine.say(choose_text[0])
engine.runAndWait()

cap.release()
cv2.destroyAllWindows()

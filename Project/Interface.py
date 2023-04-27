from Hand_Detecter import Hand_Detecter as hd
from Sit_Ups import Pose_Detected as pose1
from Push_Up import Pose_Detected as pose2
from Squat import Pose_Detected as pose3
from Leg_Raises import Pose_Detected as pose4
from Jumping_Jacks import Pose_Detected as pose5
import Global_Use
import cv2
import time
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('voice', 'zh')

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

# break
count = 3
bye = 0

# for first interface
confirm = 0
has_choose = 0
last_choose = 'NAN'

# for second interface which use to choose act
vedio_confirm = 0
vedio_has_choose = 0
last_vedio_choose = 'NAN'

# for third interface which use to choose sport times
count_times_confirm = 0
count_times_choose = 0
last_times_choose = 'NAN'

# for showing the record
complete_sport = 0
accuracy_count = 0
show = 1

difficulty = [8, 15, 25]

text = ['請選擇您要做的動作', 
        '1. 仰臥起坐', '2. 伏地挺身', '3. 深蹲', '4. 仰臥抬腿', '5. 開合跳', '6. 離開',
        '您的選擇是 ', 
        '請選擇您要的操作', 
        '1. 範例影片', '2. 開始運動', '3. 回到上一頁',
        '請選擇您要做的次數', 
        '1.  '+str(difficulty[0])+' 次', '2. '+str(difficulty[1])+' 次', '3. '+str(difficulty[2])+' 次', '4. 回到上一頁'] 

choose_text = ['再見',
               '仰臥起坐', '伏地挺身', '深蹲', '仰臥抬腿', '開合跳', '離開',
               '範例影片', '開始運動', '回到上一頁',
               str(difficulty[0])+' 次', str(difficulty[1])+' 次', str(difficulty[2])+' 次', '回到上一頁',
               '您已完成 次', '準確度為 %']

'''
# for testing lag
confirm = 1
vedio_confirm = 1
last_vedio_choose = '2'
count_times_confirm = 1
last_times_choose = 2
last_choose = '1'
'''

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
        img = Global_Use.interface(img, text[0], 30)
        img = Global_Use.interface(img, text[1], 75)
        img = Global_Use.interface(img, text[2], 110)
        img = Global_Use.interface(img, text[3], 145)
        img = Global_Use.interface(img, text[4], 180)
        img = Global_Use.interface(img, text[5], 215)
        img = Global_Use.interface(img, text[6], 250)

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
        if(not vedio_confirm):
            img, choose = hd(cap)

            if(choose == '4' or choose == '5' or choose == '6'):
                choose = 'NAN'

            # choose
            img = Global_Use.interface(img, text[7] + text[int(last_choose)], 30)
            img = Global_Use.interface(img, text[8], 65)
            img = Global_Use.interface(img, text[9], 110)
            img = Global_Use.interface(img, text[10], 145)
            img = Global_Use.interface(img, text[11], 180)

            Global_Use.handpose(img, choose, imgr, imgc)

            if(not vedio_has_choose):
                if(choose == '1' or choose == '2' or choose == '3'):
                    vedio_has_choose = 1
                    last_vedio_choose = choose
                    start = time.time()

            else:
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

                elif(not nan_start and choose == 'NAN'):
                    nan_start = time.time()

                elif(nan_start):
                    nan_end = time.time()

                    if(nan_end - nan_start > wait_time):
                        vedio_has_choose = 0
                        end = 0.0
                        nan_end = 0.0

                elif(other_start):
                    other_end = time.time()

                    if(other_end - other_start > other_time):
                        vedio_has_choose = 0
                        end = 0.0
                        other_start = 0.0
                        other_end = 0.0

                elif(not other_start):
                    other_start = time.time()

        else:
            match last_vedio_choose:

                case '1':
                    match last_choose:

                        case '1':
                            pose1(cap, 1, 0, 0)
                        case '2':
                            pose2(cap, 1, 0, 0)
                        case '3': 
                            pose3(cap, 1, 0, 0)
                        case '4':
                            pose4(cap, 1, 0, 0)
                        case '5':
                            pose5(cap, 1, 0, 0)
                    
                    vedio_confirm = 0
                    vedio_has_choose = 0

                case '2':
                    if(not count_times_confirm):
                        img, choose = hd(cap)

                        if(choose == '5' or choose == '6'):
                            choose = 'NAN'

                        img = Global_Use.interface(img, text[12], 30)
                        img = Global_Use.interface(img, text[13], 75)
                        img = Global_Use.interface(img, text[14], 110)            
                        img = Global_Use.interface(img, text[15], 145)
                        img = Global_Use.interface(img, text[16], 180)

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

                            elif(other_start):
                                other_end = time.time()

                                if(other_end - other_start > other_time):
                                    count_times_choose = 0
                                    end = 0.0
                                    other_start = 0.0
                                    other_end = 0.0
                                        
                            elif(not other_start):
                                other_start = time.time()                                

                    else:
                        if(complete_sport == 100):
                            if(show):
                                img = Global_Use.forshow(img,\
                                choose_text[14][:4]+str(int(count_times))+choose_text[14][5],\
                                choose_text[15][:4]+str(int(accuracy_count))+choose_text[15][5])
                                
                                show = 0

                            else:
                                engine.say(choose_text[14][:4]+str(int(count_times))+choose_text[14][5])
                                engine.say(choose_text[15][:4]+str(int(accuracy_count))+choose_text[15][5])
                                engine.runAndWait()

                                complete_sport = 0
                                show = 1
                                confirm = 0
                                has_choose = 0
                                vedio_confirm = 0
                                vedio_has_choose = 0
                                count_times_confirm = 0
                                count_times_choose = 0
                                other_start = 0.0
                                other_end = 0.0

                        else:
                            match last_choose:
                                
                                case '1':
                                    complete_sport, count_times, accuracy_count = pose1(cap, 0, 0, choose_text[int(last_choose)])
                                case '2':
                                    complete_sport, count_times, accuracy_count = pose2(cap, 0, 0, choose_text[int(last_choose)])
                                case '3':
                                    complete_sport, count_times, accuracy_count = pose3(cap, 0, 0, choose_text[int(last_choose)])
                                case '4':
                                    complete_sport, count_times, accuracy_count = pose4(cap, 0, 0, choose_text[int(last_choose)])
                                case '5':
                                    complete_sport, count_times, accuracy_count = pose5(cap, 0, 0, choose_text[int(last_choose)])
                            
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

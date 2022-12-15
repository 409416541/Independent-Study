from PoseModule import PoseDetector
import Global_Use
import cv2

def Pose_Detected():

    '''
    cap = cv2.VideoCapture("./Project/Test_Media/Squat.mp4")

    if not cap.isOpened():
        print("Cannot open vedio")
        exit()
    ''' 

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    detector = PoseDetector()
    dir = 0  # 0: 站起  1: 蹲下
    count = 0

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                angle, img = detector.findAngle(landmarks[24], landmarks[26],
                                                landmarks[28], img)
                                                
                # 顯示進度條
                Global＿Use.thebar(img, angle, 95, 175)

                if angle <= 110:  # 目前狀態:蹲下
                    if dir == 0:  # 之前狀態:站起
                        count = count + 0.5
                        dir = 1   # 更新狀態:蹲下

                if angle >= 165:  # 目前狀態:站起
                    if dir == 1:  # 之前狀態:蹲下
                        count = count + 0.5
                        dir = 0   # 更新狀態:站起
                        
                Global＿Use.thecount(img, str(int(count)))

            cv2.imshow("landmarks", img)        
        else:
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

#Pose_Detected()
from PoseModule import PoseDetector
import Global_Use
import cv2

def Pose_Detected(cap):

    '''
    cap = cv2.VideoCapture("./Project/Test_Media/leg_raises.mp4")

    if not cap.isOpened():
        print("Cannot open video")
        exit()
    '''
    
    '''
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()  
    '''

    detector = PoseDetector()
    dir = 1  # 0: 抬腿 1: 躺著
    count = 0

    while True:
        success, img = cap.read()

        if success:
            landmarks, img = detector.findPose(img, draw=True)

            if landmarks:
                angle1, img = detector.findAngle(landmarks[12], landmarks[24],
                                                landmarks[26], img)
                angle2, img = detector.findAngle(landmarks[24], landmarks[26],
                                                landmarks[28], img)

                # 顯示進度條
                Global_Use.thebar(img, angle1, 90, 180)

                # 目前狀態::抬腿
                if angle2 <= 180 and angle2 >= 155 and angle1 >= 155 and angle1 <= 180:
                    if dir == 0:   # 之前狀態:抬腿
                        count = count + 0.5
                        dir = 1    # 更新狀態:躺著

                # 目前狀態::躺著
                if angle2 <= 180 and angle2 >= 155 and angle1 >= 75 and angle1 <= 90:
                    if dir == 1:   # 之前狀態:躺著
                        count = count + 0.5
                        dir = 0    # 更新狀態:抬腿

                Global_Use.thecount(img, str(int(count)))

            return img
            #cv2.imshow("Leg Raises", img)

        else:
            break

        '''
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    '''

#Pose_Detected()

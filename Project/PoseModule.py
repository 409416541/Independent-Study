import cv2
import mediapipe as mp
import math

'''
The reference from cvzone
URL : https://www.computervision.zone/lessons/code-files-14/
Title : PoseModule.py
'''

class PoseDetector:
    def __init__(self, mode=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)
        self.lmList = [] 

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        landmarks = []
        if self.results.pose_landmarks:
            for _, landmark in enumerate(self.results.pose_landmarks.landmark):
                h, w = img.shape[:2]
                x, y = int(landmark.x * w), int(landmark.y * h)
                landmarks.append([x, y])

            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
                
        return landmarks, img

    def findAngle(self, all_angle, img=None):
        calculate = []

        for i in range(int(len(all_angle)/3)):
            x1, y1 = all_angle[i * 3]
            x2, y2 = all_angle[i * 3 + 1]
            x3, y3 = all_angle[i * 3 + 2]

            '''# Get the landmarks
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3'''

            # Calculate the Angle
            angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                math.atan2(y1 - y2, x1 - x2))
            if angle < 0:
                angle += 360
                
            if angle > 180:
                angle = 360 - angle

            calculate.append(angle)

        '''if img is not None:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 1)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 1)
            cv2.circle(img, (x1, y1), 4, (240, 222, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 8, (240, 222, 0), 2)
            cv2.circle(img, (x2, y2), 7, (230, 0, 111), cv2.FILLED)
            cv2.circle(img, (x2, y2), 11, (230, 0, 111), 2)
            cv2.circle(img, (x3, y3), 4, (240, 222, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 8, (240, 222, 0), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (91, 183, 240), 2)'''
        return calculate

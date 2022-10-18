import cv2
import numpy as np

def thebar(img, angle, a, b):
    bar = np.interp(angle, (a, b), (50, 250))
    cv2.rectangle(img, (50, 30), (int(bar), 40),
                        (0, 255, 0), cv2.FILLED)

def thetext(img, count):
    cv2.putText(img, count, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 255), 5)
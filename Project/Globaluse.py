import cv2
import numpy as np

def thebar(img, angle, a, b):
    bar = np.interp(angle, (a, b), (50, 250))
    cv2.rectangle(img, (50, 20), (int(bar), 40),
                        (91, 245, 150), cv2.FILLED)

def thecount(img, count):       
    cv2.putText(img, count, (20, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 
               1, (240, 92, 186), 5)


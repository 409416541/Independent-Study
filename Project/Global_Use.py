import cv2
import numpy as np

def thebar(img, angle, a, b):
    bar = np.interp(angle, (a, b), (50, 250))
    cv2.rectangle(img, (60, 28), (int(bar), 48), (91, 245, 150), cv2.FILLED)

def thecount(img, count):       
    cv2.putText(img, count, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (240, 92, 186), 3)

def interface(img, text, y):
    cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))

def confirm(img, text, y):
    cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (0, 245, 146))

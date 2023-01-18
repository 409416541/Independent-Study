import cv2
import numpy as np

def thebar(img, angle, a, b):
    bar = np.interp(angle, (a, b), (60, 260))
    cv2.rectangle(img, (60, 28), (int(bar), 48), (91, 245, 150), cv2.FILLED)

def thecount(img, count):       
    cv2.putText(img, count, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (240, 92, 186), 3)

def accuracy(img, count):       
    cv2.putText(img, count, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (240, 92, 186), 3)

def whatsportnow(img, text, row):
    cv2.putText(img, text, (10, row-20), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 78, 250), 2)

def interface(img, text, row):
    cv2.putText(img, text, (10, row), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))

def byebyecount(img, count, row, col):
    cv2.putText(img, count, (row//2 -4, col//2 - 4), cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 0, 255), 20)

def handpose(img, text, row, col):
    col -= 50

    if(text == 'NAN'):
        col -= 25

    cv2.putText(img, text, (col, row-20), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.8, (35, 78, 250), 1)

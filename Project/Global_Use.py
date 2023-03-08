import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

'''

img = np.zeros((150,300,3), dtype='uint8')   # 繪製黑色畫布
fontpath = 'NotoSansTC-Regular.otf'          # 設定字型路徑
font = ImageFont.truetype(fontpath, 50)      # 設定字型與文字大小
imgPil = Image.fromarray(img)                # 將 img 轉換成 PIL 影像
draw = ImageDraw.Draw(imgPil)                # 準備開始畫畫
draw.text((0, 0), '大家好～\n嘿嘿嘿～', fill=(255, 255, 255), font=font)  # 畫入文字，\n 表示換行
img = np.array(imgPil)

'''

def thecount(img, count):       
    cv2.putText(img, count, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (240, 92, 186), 3)

def sport(img, angle, a, b, count, accuracy, displacement, text, col, row):
    bar = np.interp(angle, (a, b), (60, 260))
    cv2.rectangle(img, (60, 28), (int(bar), 48), (91, 245, 150), cv2.FILLED)
    #cv2.putText(img, count, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (240, 92, 186), 3)
    #cv2.putText(img, accuracy, (col-displacement, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 92, 186), 2)
    #cv2.putText(img, text, (10, row-20), cv2, 1, (0, 78, 250), 2)

    fontpath = './Project/NotoSansTC-Regular.otf'
    imgPil = Image.fromarray(img)
    draw = ImageDraw.Draw(imgPil)
    draw.text((10, 10), count, fill=(240, 92, 186), font=ImageFont.truetype(fontpath, 40))
    draw.text((col-displacement, 5), accuracy, fill=(240, 92, 186), font=ImageFont.truetype(fontpath, 35))
    draw.text((10, row-45), text, fill=(0, 78, 250), font=ImageFont.truetype(fontpath, 25))
    img = np.array(imgPil)

    return img
    
def interface(img, text, row):
    fontpath = './Project/NotoSansTC-Regular.otf'
    imgPil = Image.fromarray(img)
    draw = ImageDraw.Draw(imgPil)
    draw.text((10, row), text, fill=(245, 206, 96), font=ImageFont.truetype(fontpath, 20))
    img = np.array(imgPil)

    return img

    #cv2.putText(img, text, (10, row), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (245, 206, 96))

def byebyecount(img, count, row, col):
    cv2.putText(img, count, (row//2 -4, col//2 - 4), cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 0, 255), 20)

def handpose(img, text, row, col):
    col -= 50

    if(text == 'NAN'):
        col -= 25

    cv2.putText(img, text, (col, row-20), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.8, (35, 78, 250), 1)

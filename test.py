import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image    # 載入 PIL 相關函式庫

def test(img):
    fontpath = './NotoSansTC-Regular.otf'          # 設定字型路徑
    font = ImageFont.truetype(fontpath, 50)      # 設定字型與文字大小
    imgPil = Image.fromarray(img)                # 將 img 轉換成 PIL 影像
    draw = ImageDraw.Draw(imgPil)                # 準備開始畫畫
    draw.text((0, 0), '大家好～\n嘿嘿嘿～', fill=(255, 255, 255), font=font)  # 畫入文字，\n 表示換行
    img = np.array(imgPil)                       # 將 PIL 影像轉換成 numpy 陣列
    return img

for i in range(int(24/3)):
    print(i * 3)
    print(i * 3 + 1)
    print(i * 3 + 2)

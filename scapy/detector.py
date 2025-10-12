# 检查图片中是否有人脸
import cv2
import os

ROOT = 'E:\\PyCharm 2022.3.3\\study\\python blackhat\\scapy\\test\\pictures'
FACES = 'E:\\PyCharm 2022.3.3\\study\\python blackhat\\scapy\\test\\faces'
TRAIN = 'E:\\PyCharm 2022.3.3\\study\\python blackhat\\scapy\\test\\training'


def detect(srcdir=ROOT, tgtdir=FACES, train_dir=TRAIN):
    for fname in os.listdir(srcdir):
        if not fname.upper().endswith('.JPG'):
            continue
        fullname = os.path.join(srcdir, fname)
        newname = os.path.join(tgtdir, fname)
        img = cv2.imread(fullname)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        training = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        cascade = cv2.CascadeClassifier(training)
        rects = cascade.detectMultiScale(gray, 1.3, 5)
        try:
            if rects.any():
                print('Got a face')
                rects[:, 2:] += rects[:, :2]
        except AttributeError:
            print(f'No faces found in {fname}.')
            continue

        # 在图片上标注脸
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
        cv2.imwrite(newname, img)


if __name__ == '__main__':
    detect()

import numpy
import cv2
import os
import time
import sys

try:
    cv2data = os.path.join(cv2.__path__[0], 'data')
    cascadepath = os.path.join(cv2data, 'haarcascade_frontalface_default.xml')

    cascade = cv2.CascadeClassifier(cascadepath)  # Загрузка файла каскада

    # Проверка: загружен ли каскад
    if cascade.empty():
        sys.exit('Failed to load cascade')

    path: str
    # Командная строка
    if len(sys.argv) > 1:
        path = sys.argv[1]  # путь к файлу
    else:
        path = input()

    video = cv2.VideoCapture(path)
    for attempt in range(100):
        if video.isOpened():
            break
        else:
            time.sleep(0.1)
    else:
        sys.exit('Could not open video')

    scale_per_step = 1.3  # В какой пропорции уменьшаем размер изображения
    min_neighbours = 5  # Будем возвращать любой силбный отклик

    while True:
        success, frame = video.read()  # Считываем видео по кадрам
        if not success:
            print('Stream ended')
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rois = cascade.detectMultiScale(gray, scale_per_step, min_neighbours)

        # Отрисовка прямоугольника (выделение области)
        for x, y, w, h in rois:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('Found', frame)
        key = cv2.waitKeyEx()  # Код считывания нажатия клавиши
        if key == ord('w'):  # Когда W
            min_neighbours += min(20, 1)  # +
        elif key == ord('s'):  # Когда S
            min_neighbours -= max(0, 1)  # -
        elif key == 27:
            break
except:
    print("Error")
    sys.exit(1)
finally:
    video.release()
import numpy
import cv2
import os
import time
import sys
import pafy

try:
    cv2data = os.path.join(cv2.__path__[0], 'data')
    cascadepath = os.path.join(cv2data, 'haarcascade_frontalface_default.xml')  # Каскад
    cascadepath_eye = os.path.join(cv2data, 'haarcascade_eye.xml')  # Каскад

    cascade = cv2.CascadeClassifier(cascadepath)  # Загрузка файла каскада
    cascade_eye = cv2.CascadeClassifier(cascadepath_eye)  # Загрузка файла каскада

    if cascade.empty():  # Если каскад не был загружен
       sys.exit('Failed to load cascade')

    url: str
    # Командная строка
    if len(sys.argv) > 1:
        url = sys.argv[1]  # путь к файлу
    else:
        url = input()

    pafy_video = pafy.new(url)  # Загрузка видео с ютуба (получение видео-потоков)
    best = pafy_video.getbest(preftype='mp4')

    video = cv2.VideoCapture(best.url)  # Выбор лучшего потока
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
        success, frame = video.read()  # Считываем видео по кадрами
        if not success:
            print('Stream ended')
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Преобразование в оттенки серого
        rois = cascade.detectMultiScale(gray, scale_per_step, min_neighbours)

        #Отрисовка прямоугольника и эллипсов (выделение лица и глаз)
        for x, y, w, h in rois:
            face = gray[y:y + h, x:x + w]
            rois2 = cascade_eye.detectMultiScale(face, scale_per_step, min_neighbours)

            for x1, y1, w1, h1 in rois2:
                cv2.ellipse(frame, (x + x1 + w1 // 2, y + y1 + h1 // 2), (w1 // 2, h1 // 2), 0, 0, 360, (255, 64, 64),
                            3)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (64, 255, 64), 2)
        cv2.imshow('Found', frame)
        key = cv2.waitKeyEx(10)  # Считывание кода нажатой клавиши
        if key == ord('w'):  # Если нажата W
            min_neighbours += min(20, 1)  # +
            print(min_neighbours)
        elif key == ord('s'):  # Если нажата S
            min_neighbours -= max(0, 1)  # -
            print(min_neighbours)
        elif key == 27:
            break

except:
    print('Error')
    sys.exit(1)
finally:
    video.release()
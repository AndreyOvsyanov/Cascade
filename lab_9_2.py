import numpy
import cv2
import os
import time
import sys
import pafy

try:
    cv2data = os.path.join(cv2.__path__[0], 'data')
    cascadepath = os.path.join(cv2data, 'haarcascade_frontalface_default.xml')

    cascade = cv2.CascadeClassifier(cascadepath)  # Загрузка файла каскада

    if cascade.empty():
        sys.exit('Failed to load cascade')

    url: str
    # Командная строка
    if len(sys.argv) > 2:
        url = sys.argv[1]  # путь к файлу
    else:
        url = input()

    pafy_video = pafy.new(url)  # Получение списка видео-потоков со страницы
    best = pafy_video.getbest(preftype='mp4')  # Выбор лучшего потока

    video = cv2.VideoCapture(best.url)  # Загружаем вижео
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
        if not success:  # Если видео закончилось или не открылось
            print('Stream ended')
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Кадр в сером оттенке
        rois = cascade.detectMultiScale(gray, scale_per_step, min_neighbours)

        # Отрисовка прямоугольника (выделение области)
        for x, y, w, h in rois:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (64, 255, 64), 2)
        cv2.imshow('Found', frame)
        key = cv2.waitKeyEx(10)  # Считываем код нажатия клавиши

        if key == ord('w'):  # Если нажата W
            min_neighbours += min(20, 1)  # +
            print(min_neighbours)
        elif key == ord('s'):  # Есди нажата S
            min_neighbours -= max(0, 1)  # -
            print(min_neighbours)
        elif key == 27:
            break
except:
    print('Error')
    sys.exit(1)
finally:
    video.release()
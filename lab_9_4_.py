import cv2
import sys

path: str
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = input()

video = cv2.VideoCapture(path) #Загрузка видео

i: int = 1 #Переменная для подсчёта кадров

while True:
    success, frame = video.read() #Считываем видео по кадрам
    if not success:
        raise IOError('video is end / video is failed loading')

    cv2.imwrite(f'{i}frame.jpg', frame) #Покадровая запись в файл

    i += 1

    cv2.imshow("frame", frame) #Показ кадра
    if cv2.waitKey(40) == 27:
        break





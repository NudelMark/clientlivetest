import cv2

import socket

import struct

import numpy as np

# Инициализация сокета и привязка к IP-адресу и порту

TCP_IP = '192.168.1.105'
TCP_PORT = 8888

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

# Инициализация камеры

cap = cv2.VideoCapture("dev/video0")

# Установка параметров кадра

WIDTH = 640

HEIGHT = 640

VIDEO_TYPE = 'MJPG'

# Запись параметров в переменную header

header = struct.pack('iii', WIDTH, HEIGHT, cv2.VideoWriter_fourcc(*VIDEO_TYPE))

# Цикл трансляции видео

while(True):
    # Получение кадра с камеры

    ret, frame = cap.read()

    # Изменение размера кадра

    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    cv2.imshow(frame)
    # Кодирование кадра в байты

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(imgencode)
    stringData = data.tostring()

    # Отправка заголовка параметров и кадра на сервер

    sock.sendall(header)
    sock.sendall(stringData)

# Остановка камеры и закрытие соединения с сервером

cap.release()
sock.close()

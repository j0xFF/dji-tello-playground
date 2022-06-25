# DJI Tello SDK
# Face Tracker v1.1

from djitellopy import tello
from time import sleep
import cv2
import numpy as np

w, h = 640, 480
fbs_rng = [6200, 6800]
pid = [0.4, 0.4, 0]
pid_err = 0
leb = tello.Tello()
leb.connect()
print(leb.get_battery())
leb.streamoff()
leb.streamon()
leb.takeoff()
leb.send_rc_control(0, 0, 15, 0)
# sleep(1)


def find_face(img):
    face_csd = cv2.CascadeClassifier("src/haarcascade_frontalface_default.xml")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fcs = face_csd.detectMultiScale(img_gray, 1.2, 8)
    mfc_center_list = []
    mfc_area_list = []

    for (x, y, w, h) in fcs:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 3, (0, 255, 0), cv2.FILLED)
        mfc_center_list.append([cx, cy])
        mfc_area_list.append(area)

    if len(mfc_area_list) != 0:
        i = mfc_area_list.index(max(mfc_area_list))
        return img, [mfc_center_list[i], mfc_area_list[i]]
    else:
        return img, [[0, 0], 0]


def track_face(leb, info, w, pid, pid_err):
    area = info[1]
    x, y = info[0]
    fbs = 0
    err = x - w // 2
    spd = pid[0] * err + pid[1] * (err - pid_err)
    spd = int(np.clip(spd, -100, 100))

    if fbs_rng[0] < area < fbs_rng[1]:
        fbs = 0
    if area > fbs_rng[1]:
        fbs = -20
    elif area < fbs_rng[0] and area != 0:
        fbs = 20

    if x == 0:
        spd = 0
        err = 0

    print(spd, fbs)

    leb.send_rc_control(0, fbs, 0, spd)
    return err


# cpt = cv2.VideoCapture(0)

while True:
    # _, img = cpt.read()
    img = leb.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = find_face(img)
    pid_err = track_face(leb, info, w, pid, pid_err)
    # print('Center', info[0], 'Area', info[1])
    cv2.imshow('Drone', img)

    if cv2.waitKey(1) and 0xFF == ord('q'):
        leb.land()
        break

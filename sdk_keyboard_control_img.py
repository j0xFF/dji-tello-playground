# DJI Tello SDK
# Keyboard controller - Manual
# v2.1 Image feed capture added

from djitellopy import tello
from time import sleep, time
import cv2
import logging
import base_keypress as bkp

bkp.init()
leb = tello.Tello()
leb.LOGGER.setLevel(logging.ERROR)
leb.connect()
print(leb.get_battery())
global img
leb.streamoff()
leb.streamon()


def get_keyboard_input():
    fbs, rlt, upd, yaw = 0, 0, 0, 0
    spd = 50
    ito = False
    
    if bkp.get_key('UP'):
        fbs = spd
    elif bkp.get_key('DOWN'):
        fbs = -spd

    if bkp.get_key('RIGHT'):
        rlt = spd
    elif bkp.get_key('LEFT'):
        rlt = -spd

    if bkp.get_key('w'):
        upd = spd
    elif bkp.get_key('s'):
        upd = -spd

    if bkp.get_key('a'):
        yaw = -spd
    elif bkp.get_key('d'):
        yaw = spd

    if bkp.get_key('SPACE') and not ito:
        leb.takeoff()
        ito = True

    if bkp.get_key('SPACE') and ito:
        leb.land()
        ito = False
        sleep(3)

    if bkp.get_key('z'):
        cv2.imwrite(f'src\img\{time()}.jpg', img)
        sleep(0.5)

    return [fbs, rlt, upd, yaw, ito]


while True:
    vals = get_keyboard_input()
    leb.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    # print(leb.get_height())
    # print(leb.get_distance_tof())
    print(leb.get_speed_x())
    # print(leb.get_speed_y())
    # print(leb.get_speed_z())
    # print('-----')
    img = leb.get_frame_read().frame
    img = cv2.resize(img, (800, 600))
    # img = cv2.resize(img, (1240, 720))
    cv2.imshow('Drone', img)
    cv2.waitKey(1)

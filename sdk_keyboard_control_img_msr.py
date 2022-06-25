# DJI Tello SDK
# Keyboard controller - Manual
# v3.0 Distance measurement added.

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
global dst
leb.streamon()


def get_keyboard_input():
    fbs, rlt, upd, yaw = 0, 0, 0, 0
    spd = 50
    ito = False
    # imp = False
    mp_id = 0
    
    if bkp.get_key('UP'):
        fbs = spd
        print("Speed: ", leb.get_speed_x())
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

    if bkp.get_key('o'):
        leb.enable_mission_pads()
        print('Mission Pad detection on')

    if bkp.get_key('p'):
        leb.disable_mission_pads()
        print('Mission Pad detection off')

    if bkp.get_key('l'):
        mp_id = leb.get_mission_pad_id()

    return [fbs, rlt, upd, yaw, ito, mp_id]


while True:
    vals = get_keyboard_input()
    leb.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    print("New Pad: ", vals[5])
    # print("Height: ", leb.get_height())
    # print("TOF: ", leb.get_distance_tof())
    # print("Bar: ", leb.get_barometer())
    # print('-----')
    if vals[5] == 1:
        dst = leb.get_mission_pad_distance_x()
        print("Current distance: ", dst)
    if vals[5] == 2:
        print("Distance: ", dst)
        leb.land()
        leb.end()
    img = leb.get_frame_read().frame
    img = cv2.resize(img, (800, 600))
    cv2.imshow('Drone', img)
    cv2.waitKey(1)

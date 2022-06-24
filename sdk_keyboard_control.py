# DJI Tello SDK
# Keyboard control - Manual

from djitellopy import tello
from time import sleep
import base_keypress as bkp

bkp.init()
leb = tello.Tello()
leb.connect()
print(leb.get_battery())


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

    return [fbs, rlt, upd, yaw, ito]


while True:
    vals = get_keyboard_input()
    leb.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)

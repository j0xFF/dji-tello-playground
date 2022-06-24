# DJI Tello SDK
# Basic movements - Auto

from djitellopy import tello
from time import sleep

leb = tello.Tello()
leb.connect()
print(leb.get_battery())

leb.takeoff()
leb.send_rc_control(0, 50, 0, 0)
sleep(2)
leb.send_rc_control(0, 0, 0, 30)
sleep(2)
leb.send_rc_control(0, 0, 0, 0)
leb.land()

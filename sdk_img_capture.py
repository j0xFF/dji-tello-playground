# DJI Tello SDK
# Image feed capture - Loop

from djitellopy import tello
import cv2

leb = tello.Tello()
leb.connect()
print(leb.get_battery())

leb.streamon()

while True:
    img = leb.get_frame_read().frame
    img = cv2.resize(img, (600, 450))
    cv2.imshow('Drone', img)
    cv2.waitKey(1)

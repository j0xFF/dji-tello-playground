from djitellopy import tello
from time import sleep
from pynput import keyboard
import cv2

''' right/left, forward/backward, up/down, yaw right/left (100/-100) '''

leb = tello.Tello()
leb.connect()
print(leb.get_battery())
controls_list = ['w', 's', 'a', 'd']


def on_press(key):
    try:
        if key.char == 'w':
            print("going forward...")
        elif key.char == 's':
            print("going backwards...")
        elif key.char == 'a':
            print("going leftwards...")
        elif key.char == 'd':
            print("going rightwards...")

        print('\n')

    except AttributeError:
        if key == keyboard.Key.space:
            print("\ntaking off...")

        if key == keyboard.Key.ctrl_l:
            print("\nlanding...")

        if key == keyboard.Key.up:
            print("\nthrottling up...")

        if key == keyboard.Key.down:
            print("\nthrottling down...")

        if key == keyboard.Key.left:
            print("\nyawing leftwards...")

        if key == keyboard.Key.right:
            print("\nyawing rightwards...")
            

def on_release(key, is_takeoff):
    if key == keyboard.Key.esc:
        print("exiting...")
        print(leb.get_battery())
        leb.land()
        return False

    if key == keyboard.Key.space:
        leb.takeoff()
        
    if key == keyboard.Key.ctrl_l:
        print(leb.get_battery())
        leb.land()

    if key == keyboard.Key.up:
        leb.send_rc_control(0, 0, 20, 0)
        sleep(2)
        leb.send_rc_control(0, 0, 0, 0)

    if key == keyboard.Key.down:
        leb.send_rc_control(0, 0, -20, 0)
        sleep(2)
        leb.send_rc_control(0, 0, 0, 0)

    if key == keyboard.Key.left:
        leb.send_rc_control(0, 0, 0, -60)
        sleep(1)
        leb.send_rc_control(0, 0, 0, 0)

    if key == keyboard.Key.right:
        leb.send_rc_control(0, 0, 0, 60)
        sleep(1)
        leb.send_rc_control(0, 0, 0, 0)

    if 'char' in dir(key):
        if key.char not in controls_list:
            print("NOP")

        if key.char == 'w':
            leb.send_rc_control(0, 20, 0, 0)
            sleep(2)
            leb.send_rc_control(0, 0, 0, 0)

        if key.char == 's':
            leb.send_rc_control(0, -20, 0, 0)
            sleep(2)
            leb.send_rc_control(0, 0, 0, 0)

        if key.char == 'a':
            leb.send_rc_control(-20, 0, 0, 0)
            sleep(2)
            leb.send_rc_control(0, 0, 0, 0)

        if key.char == 'd':
            leb.send_rc_control(20, 0, 0, 0)
            sleep(2)
            leb.send_rc_control(0, 0, 0, 0)


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

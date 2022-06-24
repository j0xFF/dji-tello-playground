# Pygame - Key pressing detection

import pygame


def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def get_key(kname):
    ans = False

    for i in pygame.event.get():
        pass

    kin = pygame.key.get_pressed()
    mkey = getattr(pygame, 'K_{}'.format(kname))

    if kin[mkey]:
        ans = True

    pygame.display.update()
    return ans


def main():
    if get_key('UP'):
        print("Moving forwards...")

    if get_key('DOWN'):
        print("Moving backwards...")

    if get_key('RIGHT'):
        print("Moving rightwards...")
        
    if get_key('LEFT'):
        print("Moving leftwards...")


if __name__ == '__main__':
    init()
    while True:
        main()

#!/usr/bin/python

import time
import pygame, sys
from pygame.locals import *

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

#How it all starts
pygame.init()

#desired framrate
FPS = 30
fpsClock = pygame.time.Clock()

#Music comes into play
soundObj = pygame.mixer.Sound('wscream.ogg')
soundObj.play()
time.sleep(1) # wait and let the sound play for 1 second
soundObj.stop()


#drawing size
SCREEN = pygame.display.set_mode((500,400),0,32)

dongleImg = pygame.image.load('dongle.png')
dongleX = 5
dongleY = 5
direction = 'right'

start_rect = dongleImg.get_rect()
image_rect = start_rect

fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('KILL THE DONGLE!', True, RED, BLACK)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)


#pygame.draw.polygon(SCREEN, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

while True:
    pygame.display.set_caption(direction + " dongleX: " + str(dongleX) + " dongleY: " + str(dongleY))
    SCREEN.fill(WHITE)

    event = pygame.event.poll()
    keyinput = pygame.key.get_pressed()

    # exit on corner 'x' click or escape key press
    if keyinput[pygame.K_ESCAPE]:
                raise SystemExit

    if direction == 'right':
        dongleX += 5
        if dongleX > 280:
            pygame.display.set_caption("OMGOMGOMG")
            direction = 'down'
    elif direction == 'down':
        dongleY += 5
        if dongleY == 220:
            direction = 'left'
    elif direction == 'left':
        dongleX -= 5
        if dongleX == 10:
            direction = 'up'
    elif direction == 'up':
        dongleY -= 5
        if dongleY == 10:
            direction = 'right'

    SCREEN.blit(dongleImg, (dongleX, dongleY))
    SCREEN.blit(textSurfaceObj, textRectObj)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = list(event.pos)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Test for 'collision'
            if dongleX - 10 < mouse_x < dongleX + dongleImg.get_width() and dongleY - 10 < mouse_y < dongleY + dongleImg.get_height():
                pygame.display.set_caption("DONGLE HIT!")
                soundObj.play()
                time.sleep(1) # wait and let the sound play for 1 second
                soundObj.stop()

    pygame.display.update()
    fpsClock.tick(FPS)

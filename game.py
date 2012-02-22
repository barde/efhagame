#!/usr/bin/python

import time, random
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
background = pygame.image.load('irc.png')
SCREEN = pygame.display.set_mode((1280, 800), pygame.FULLSCREEN)
#background = background.convert_alpha()

dongleImg = pygame.image.load('dongle.png')
dongleX = random.randint(0,1000)
dongleY = random.randint(0,800)
direction = 'right'

start_rect = dongleImg.get_rect()
image_rect = start_rect

fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('KILL THE DONGLE!', True, RED, BLACK)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)

cursize = [background.get_width(), background.get_height()]

#pygame.draw.polygon(SCREEN, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

while True:

    pygame.display.set_caption(direction + " dongleX: " + str(dongleX) + " dongleY: " + str(dongleY))

    ircimage = pygame.transform.smoothscale(background, cursize)
    imgpos = ircimage.get_rect(centerx=640, centery=400)
    SCREEN.fill(BLACK)
    SCREEN.blit(ircimage,imgpos) 

    event = pygame.event.poll()
    keyinput = pygame.key.get_pressed()

    # exit on corner 'x' click or escape key press
    if keyinput[pygame.K_ESCAPE]:
                raise SystemExit

    randomStep = random.randint(0,5) + 3
    #either move erratically
    if random.getrandbits(1) == 1:
        rand = random.getrandbits(3)
        if rand ==  0:
            dongleX += randomStep
        elif rand == 1:
            dongleY -= randomStep
        elif rand == 1:
            dongleX -= randomStep
            dongleY += randomStep
    #else move in a circle around the screen
    else:
        if direction == 'right':
            dongleX += randomStep
            if dongleX > cursize[0] - dongleImg.get_height() * 2 :
                pygame.display.set_caption("OMGOMGOMG")
                direction = 'down'
        elif direction == 'down':
            dongleY += randomStep
            if dongleY > cursize[1] - dongleImg.get_width() * 2:
                direction = 'left'
        elif direction == 'left':
            dongleX -= randomStep
            if dongleX < 10:
                direction = 'up'
        elif direction == 'up':
            dongleY -= randomStep
            if dongleY < 10:
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

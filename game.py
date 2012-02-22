#!/usr/bin/python
#2012 Bartholomaeus Dedersen
#A game
#Honourable mention: Designer of Tannenberg Font
#                    PyGame crew

import time, random
import pygame, sys
import thread
from pygame.locals import *

#most important:
randomStep = 0
random2Bit = 0

def devote_offerings_to_rng():
    global randomStep, random2Bit
    randomStep = random.randint(0,5) + 3
    random2Bit = random.getrandbits(2)

devote_offerings_to_rng()

######
#Init all stuff
# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

#How it all starts
pygame.init()

#desired framrate
FPS = 70
fpsClock = pygame.time.Clock()

#Music comes into play
soundObj = pygame.mixer.Sound('wscream.ogg')
backgroundSong = pygame.mixer.Sound('bckground.ogg')
thread.start_new_thread(backgroundSong.play,())


#drawing size
resolution = [1280, 800]
background = pygame.image.load('irc.png')
SCREEN = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
#background = background.convert_alpha()

#the desired graphics primitive gets alpha channeled if png with per pixel transparency
dongleImg = pygame.image.load('dongle.png').convert_alpha()
#put it somewhere on the screen
dongleX = random.randint(0,resolution[0] - dongleImg.get_width() * 2)
dongleY = random.randint(0,resolution[1] - dongleImg.get_height() * 2)
#and let it go in some direction
directions = ['right', 'left', 'up', 'down']
direction = directions[random2Bit]

start_rect = dongleImg.get_rect()
image_rect = start_rect

fontObj = pygame.font.Font('ts.ttf', 42)
textSurfaceObj = fontObj.render('GLOCK THE DONGLE!', True, RED, BLACK)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (400, 250)

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

    devote_offerings_to_rng()
    #either move erratically
    if random2Bit == 1:
        devote_offerings_to_rng()
        if random2Bit ==  0:
            dongleX += randomStep
        elif random2Bit == 1:
            dongleY -= randomStep
        elif random2Bit == 2:
            dongleX -= randomStep
        elif random2Bit == 3:
            dongleY += randomStep
    elif random2Bit == 2:
        devote_offerings_to_rng()
        if random2Bit == 0:
            direction = directions[random2Bit]
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

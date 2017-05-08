import pygame
from pygame.locals import *

class Animation:

    def __init__(s, image, posX, posY, width, height, numberOfImage, annimationDuration):

        X = pygame.display.Info().current_w/2560
        Y = pygame.display.Info().current_h/1440

        s.listImages = []
        s.frame = 0
        s.time = 0
        s.timeBetweenFrame = annimationDuration/numberOfImage
		

        for n in range(numberOfImage):
            s.listImages.append(image.subsurface(n*width*X+posX*X, posY*Y, width*X, height*Y))

    def update(s, screen, deltaTime, rect):

        s.time += deltaTime
        if s.time >= s.timeBetweenFrame:
            s.time = 0
            s.frame += 1
            if s.frame == len(s.listImages):
                s.frame = 0
    
        screen.blit(s.listImages[s.frame], rect)
		
    def Reset(s):
	
        s.frame = 0
        s.time = 0

    def get_rect(s):

        return s.listImages[0].get_rect()


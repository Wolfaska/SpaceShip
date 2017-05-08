import pygame 
from pygame.locals import *
import sys, os

def GetControlersData(cData):

    for event in pygame.event.get():

        if event.type == MOUSEMOTION:
            cData['MOUSEX'] = event.pos[0]
            cData['MOUSEY'] = event.pos[1]

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                cData['LEFTBUTTON'] = True
            elif event.button  == 3:
                cData['RIGHTBUTTON'] = True
                
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                cData['LEFTBUTTON'] = False
            elif event.button  == 3:
                cData['RIGHTBUTTON'] = False
                
        elif event.type == KEYDOWN:
            if event.key == K_w:
                cData["Z"] = True
            elif event.key == K_s:
                cData["S"] = True
            elif event.key == K_a:
                cData["Q"] = True
            elif event.key == K_d:
                cData["D"] = True
            elif event.key == K_SPACE:
                cData["SPACE"] = True
            elif event.key == K_ESCAPE:
                cData["ESCAPE"] = True
            elif event.key == K_RETURN:
                cData ['ENTER'] = True
            
            
        elif event.type == KEYUP:
            if event.key == K_w:
                cData["Z"] = False
            elif event.key == K_s:
                cData["S"] = False
            elif event.key == K_a:
                cData["Q"] = False
            elif event.key == K_d:
                cData["D"] = False
            elif event.key == K_SPACE:
                cData["SPACE"] = False
            elif event.key == K_ESCAPE:
                cData["ESCAPE"] = False
            elif event.key == K_RETURN:
                cData ['ENTER'] = False    

def LoadImage(imageName, alpha=False, posX = 0, posY = 0, w = 0, h = 0):#définition du chargement des images
    
    try:
        X = pygame.display.Info().current_w/2560
        Y = pygame.display.Info().current_h/1440

        if alpha:
            image=pygame.image.load(os.path.join('data',imageName)).convert_alpha()
        else:
            image=pygame.image.load(os.path.join('data',imageName)).convert()

        imageRect = image.get_rect()    

        if (w and h) != 0:
            image1 = image.subsurface((posX, posY, w, h))
            image = pygame.transform.scale(image1, (round(imageRect.w*X/2), round(imageRect.h*Y)))
            
            return image
            
        image1 = pygame.transform.scale(image, (round(imageRect.w*X), round(imageRect.h*Y)))

        return image1
    
    except pygame.error:
        print("Erreur lors du chargement de {}".format(imageName))
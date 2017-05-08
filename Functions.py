import pygame 
from pygame.locals import *
import sys, os

def GetControlersData(cData): #définition des boutons que le joueur va utiliser pour jouer au jeu

    for event in pygame.event.get():
#déplacement de la souris sur l'écran
        if event.type == MOUSEMOTION:
            cData['MOUSEX'] = event.pos[0]
            cData['MOUSEY'] = event.pos[1]
#évènement lorsque le joueur clique sur la souris
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                cData['LEFTBUTTON'] = True
            elif event.button  == 3:
                cData['RIGHTBUTTON'] = True
#évènement lorsque le joueur ne clique PAS sur la souris                
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                cData['LEFTBUTTON'] = False
            elif event.button  == 3:
                cData['RIGHTBUTTON'] = False
#évènement lorsque le joueur appuie sur une touche de clavier                
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
            
#évènement lorsque le joueur n'appuie PAS sur une touche de clavier            
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

def LoadImage(imageName, alpha=False, posX = 0, posY = 0, w = 0, h = 0):#permet de chager les images du jeu
    
    try:
        X = pygame.display.Info().current_w/2560# variable permettant d'adapter l'image en fonction de l'écran
        Y = pygame.display.Info().current_h/1440

        if alpha:
            image=pygame.image.load(os.path.join('data',imageName)).convert_alpha()#permet de reduire le temps d'affichage de l'image
        else:
            image=pygame.image.load(os.path.join('data',imageName)).convert()#permet de reduire le temps d'affichage de l'image

        imageRect = image.get_rect()    

        if (w and h) != 0:
            image1 = image.subsurface((posX, posY, w, h))# permet de ne prendre qu'une seule région de l'image
            image = pygame.transform.scale(image1, (round(imageRect.w*X/2), round(imageRect.h*Y)))#redimentionnement de l'image en fonction de l'écran
            
            return image
            
        image1 = pygame.transform.scale(image, (round(imageRect.w*X), round(imageRect.h*Y)))

        return image1
    
    except pygame.error:
        print("Erreur lors du chargement de {}".format(imageName))

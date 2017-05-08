import pygame
from pygame.locals import *

class Button(pygame.sprite.Sprite):

    def __init__(s, buttonState1, buttonState2, posX, posY):
        
        pygame.sprite.Sprite.__init__(s)
        s.buttonState1 = buttonState1#état normal du bouton
        s.buttonState2 = buttonState2# état du bouton quand la souris le survole
        

        s.rect = s.buttonState1.get_rect()
        s.rect.move_ip(posX, posY)

        s.clicked = False

    def update(s, screen, cData): # teste si le bouton a éte cliqué et si il est survolé par la souris

        if cData['MOUSEX'] >= s.rect.x and cData['MOUSEX'] <= s.rect.x + s.rect.w and cData['MOUSEY'] >= s.rect.y and cData['MOUSEY'] <= s.rect.y + s.rect.h and cData['LEFTBUTTON']:
            s.clicked = True
            
            
        elif cData['MOUSEX'] >= s.rect.x and cData['MOUSEX'] <= s.rect.x + s.rect.w and cData['MOUSEY'] >= s.rect.y and cData['MOUSEY'] <= s.rect.y + s.rect.h:
            s.clicked = False
            screen.blit(s.buttonState2, s.rect)
            
        else:
            s.clicked = False
            screen.blit(s.buttonState1, s.rect)

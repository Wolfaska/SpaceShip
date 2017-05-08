import pygame 
from pygame.locals import *
from random import randint
from Functions import *


     
class MissileItem(pygame.sprite.Sprite):

    def __init__(s, missileItemImage):
        
        pygame.sprite.Sprite.__init__(s)
        s.spawned = False
        s.image = missileItemImage
        s.rect = s.image.get_rect()
        
        
    def Spawn(s):
        s.spawned = True
        s.rect.x = pygame.display.Info().current_w
        s.rect.y = randint(0,pygame.display.Info().current_h - s.rect.h)       

    def update(s, screen, deltaTime, ship):
        
        if s.spawned:
            if s.rect.colliderect(ship.rect):
                ship.missileActivated = True
                s.spawned = False
                ship.ammunition += 20
            elif s.rect.x + s.rect.w <= 0:
                s.spawned = False
                
            s.rect.move_ip(-0.6*deltaTime, 0)
            screen.blit(s.image, s.rect)

class ShieldItem(pygame.sprite.Sprite):

    def __init__(s, shieldImage):
        
        pygame.sprite.Sprite.__init__(s)
        s.spawned = False
        s.image = shieldImage
        s.rect = s.image.get_rect()
        
    def Spawn(s):
        s.spawned = True
        s.rect.x = pygame.display.Info().current_w
        s.rect.y = randint(0,pygame.display.Info().current_h - s.rect.h)       

    def update(s, screen, deltaTime, ship):
        
        if s.spawned:
            if s.rect.colliderect(ship.rect):
                ship.shieldActivated = True
                s.spawned = False
            elif s.rect.x + s.rect.w <= 0:
                s.spawned = False
                
            s.rect.move_ip(-0.6*deltaTime, 0)
            screen.blit(s.image, s.rect)

class NuclearMissileItem(pygame.sprite.Sprite):

    def __init__(s, nuclearMissileItemImage):
        
        pygame.sprite.Sprite.__init__(s)
        s.spawned = False
        s.image = nuclearMissileItemImage
        s.rect = s.image.get_rect()
        
    def Spawn(s):
        s.spawned = True
        s.rect.x = pygame.display.Info().current_w
        s.rect.y = randint(0,pygame.display.Info().current_h - s.rect.h)       

    def update(s, screen, deltaTime, ship):
        
        if s.spawned:
            if s.rect.colliderect(ship.rect):
                ship.nuclearMissileActivated = True
                s.spawned = False
            elif s.rect.x + s.rect.w <= 0:
                s.spawned = False
                
            s.rect.move_ip(-0.6*deltaTime, 0)
            screen.blit(s.image, s.rect)

import pygame 
from pygame.locals import *
import sys, os
from random import randint
from Functions import *
from Animation import *
from math import ceil


class Ship(pygame.sprite.Sprite):
    #créé le vaiseau
    
    def __init__(s, posX, posY, animationImage, imageHeart, missileItemImage):
        
        pygame.sprite.Sprite.__init__(s) #appel du constructeur de pygame.sprite.Sprite
        s.anim = Animation(animationImage, 0 ,0, 132, 50, 4, 300)
        s.rect = s.anim.get_rect()
        s.rect.move_ip(posX, posY)
        s.life = 3
        s.heart = imageHeart.subsurface(0, 0, 50*pygame.display.Info().current_w/2560, 50*pygame.display.Info().current_h/1440)
        s.shieldHeart = imageHeart.subsurface(50*pygame.display.Info().current_w/2560, 0,50*pygame.display.Info().current_w/2560, 50*pygame.display.Info().current_h/1440)
        s.heartRect = s.heart.get_rect()
        s.invulnerabilityTime = 0
        s.ammunition = 0
        s.missileItemImage = missileItemImage
        s.missileItemImageRect = s.missileItemImage.get_rect()

        s.shieldActivated = False
        s.nuclearMissileActivated = False

    def Hit(s):

        if s.shieldActivated:
            s.shieldActivated = False
            s.invulnerabilityTime = 1500
             
        if s.invulnerabilityTime < 0:
            s.life -= 1
            s.invulnerabilityTime = 1500
            
    def update(s, screen, deltaTime, cData):
        
        s.invulnerabilityTime -= deltaTime
        
        #gestion des deplacements du vaiseau:
        x = 0.8*(cData["D"] - cData["Q"])*deltaTime# True = 1, False = 0 
        y = 0.8*(cData["S"] - cData["Z"])*deltaTime
        if (s.rect.x + s.rect.w >= pygame.display.Info().current_w  and cData["D"]) or (s.rect.x <= 0 and cData["Q"]):
            x = 0
        if (s.rect.y + s.rect.h >= pygame.display.Info().current_h and cData["S"]) or (s.rect.y <=0 and cData["Z"]):
            y = 0
        s.rect.move_ip(x, y)

        s.anim.time += deltaTime
        if s.invulnerabilityTime > 0 and s.invulnerabilityTime%200 > 100:
            pass
        else:
            s.anim.update(screen, 0, s.rect)
            
        #affichage des vies restante du vaisseau   
        for i in range(s.life):
            if not s.shieldActivated:
                screen.blit(s.heart, (s.heartRect.x + i*s.heartRect.w,s.heartRect.y))
            else:
                screen.blit(s.shieldHeart, (s.heartRect.x + i*s.heartRect.w,s.heartRect.y))
                

class Missile(pygame.sprite.Sprite):        
    #créé les missiles
    
    def __init__(s, posX, posY, animationImage): 
            
        pygame.sprite.Sprite.__init__(s)#appel du constructeur de pygame.sprite.Sprite
        s.anim = Animation(animationImage, 0, 50, 85, 20, 2, 100)
        s.rect = s.anim.get_rect()
        s.rect.move_ip(posX, posY)
        
        
    def update(s, screen, deltaTime):
        if s.rect.x >= pygame.display.Info().current_w:
            s.kill()
        s.rect.move_ip(1.1*deltaTime,0)
        s.anim.update(screen, deltaTime, s.rect)

class Enemy(pygame.sprite.Sprite):
    #créé les astéroides
    
    def __init__(s, enemeyShipImage):

        pygame.sprite.Sprite.__init__(s) #appel du constructeur de pygame.sprite.Sprite
        s.image = enemeyShipImage
        s.rect = s.image.get_rect()
        s.rect.move_ip(pygame.display.Info().current_w, randint(0,pygame.display.Info().current_h -s.rect.h))#choisit une position aleatoire de l'aseroide sur l'axe des y
        s.rotation = randint(5, 30)
        s.velocity = randint(1, 2)

    def update(s, screen, deltaTime):
        if s.rect.x + s.rect.w <= 0:
            s.kill()
        pygame.transform.rotate(s.image, s.rotation)
        s.rect.move_ip(-s.velocity*0.7*deltaTime, 0)
        screen.blit(s.image, s.rect)

class Background:
    #permet le defilement de l'arrière plan
    def __init__(s, spaceImage):

        pygame.sprite.Sprite.__init__(s)
        s.space1 = spaceImage
        s.space1Rect = s.space1.get_rect()
        s.space2 = spaceImage
        s.space2Rect = s.space2.get_rect(topleft=(s.space1Rect.w, 0))

    def update(s, screen, deltaTime):
        
        s.space1Rect.move_ip(-0.3*deltaTime, 0)
        s.space2Rect.move_ip(-0.3*deltaTime, 0)
        if s.space1Rect.x + s.space1Rect.w < 0:
            s.space1Rect.move_ip(s.space1Rect.w + s.space2Rect.w,0)
        if s.space2Rect.x + s.space2Rect.w < 0:
            s.space2Rect.move_ip(s.space1Rect.w + s.space2Rect.w,0)
        screen.blit(s.space1, s.space1Rect)
        screen.blit(s.space2, s.space2Rect)

class Explosion(pygame.sprite.Sprite):
    #créé une explosion
    def __init__(s, rect, animationImage, explosionSound = None ):
        
        pygame.sprite.Sprite.__init__(s) 
        s.lifeTime = 200
        s.anim = Animation(animationImage, 0, 70, 100, 100, 5, 200) 
        s.rect = rect.copy()
        if explosionSound != None:
            explosionSound.play()
        
    def update(s, screen, deltaTime): #met a jour la durée de vie et la position de l'explosion
        
        s.lifeTime -= deltaTime
        if s.lifeTime <= 0:
            s.kill()
        s.rect.move_ip(-2.1*deltaTime, 0)
        s.anim.update(screen, deltaTime, s.rect)
        

class EnemyMissile(pygame.sprite.Sprite):
    #créé le missile ennemi à tête chercheuse
    
    def __init__(s, animationImage):

        pygame.sprite.Sprite.__init__(s)
        s.anim = Animation(animationImage, 0, 170 , 85, 20, 2, 100)
        s.rect = s.anim.get_rect()
        s.rect.move_ip(-s.rect.w, randint(0, pygame.display.Info().current_h) - s.rect.h)

    def update(s, screen, deltaTime, ship): #met a jour la durée de vie et la position du missile ennemi
        
        if s.rect.w > pygame.display.Info().current_w:
            s.kill() #détruit le missile quand il sort de l'écran
        y = 0
        if s.rect.x - ship.rect.x < 350 and (ship.rect.y - s.rect.y < 350 or ship.rect.y - s.rect.y > -350):
            if s.rect.y < ship.rect.y:
                y = 0.4*deltaTime
            elif s.rect.y > ship.rect.y:
                y = -0.4*deltaTime
        if ship.rect.x - s.rect.x <=0:
            y = 0
	    
        s.rect.move_ip(0.5*deltaTime,y)
        s.anim.update(screen, deltaTime, s.rect)
        
class  Shield(pygame.sprite.Sprite):
    
    def __init__(s, shieldImage):
        
        pygame.sprite.Sprite.__init__(s)
        s.image = shieldImage
        s.rect = shieldImage.get_rect()
        
    def update(s, screen, ship, shieldImage):

        if ship.shieldActivated:
            
            s.rect.x = ship.rect.x - 8
            s.rect.y = ship.rect.y - 8
            screen.blit(shieldImage,s.rect)
        
class LaserShip(pygame.sprite.Sprite):

    def __init__(s, animationImage, laserSound):

        pygame.sprite.Sprite.__init__(s)
        s.anim = Animation(animationImage, 550, 0 , 149, 99, 4, 300)
        
        s.beamLoading = Animation(animationImage, 0, 190 , 21, 70, 15, 1000)
        s.beamFireing = Animation(animationImage, 600, 190, 21, 70, 2, 200)
        s.beamRect = s.beamLoading.get_rect()
        
        s.rect = s.anim.get_rect()
        s.rect.move_ip(-s.rect.w, randint(0 , pygame.display.Info().current_h - s.rect.h))
        s.fireing = False
        s.fireingTime = 0

        s.laserSound = laserSound
        s.laserSoundPlayed = False

        s.life = 2

        s.Xmax = 1-1/randint(7,25)
        
    def beamCollide(s, rect):
        
        if ((rect.y < s.beamRect.y and rect.y + rect.h > s.beamRect.y + s.beamRect.h) or (rect.y < s.beamRect.y and rect.y + rect. h > s.beamRect.y) \
           or (rect.y + rect.h > s.beamRect.y and rect.y + rect.h < s.beamRect.y - s.beamRect.h )) and rect.x < s.beamRect.x + s.beamRect.w:
            return True
        else:
            return False
        
    def update(s, screen, deltaTime, ship, laserShipGroup):

        x, y = 0, 0

        X = pygame.display.Info().current_w/2560
        Y = pygame.display.Info().current_h/1440
            
        if s.fireingTime > 2000:
            s.beamLoading.Reset()
            s.fireing = False
            s.beamNumberOfImage = 0
            s.fireingTime = 0
            s.laserSoundPlayed = False
            
        elif s.fireing:
            s.fireingTime += deltaTime
            s.beamImageNumber = ceil(s.fireingTime/100)
            s.beamRect.x = s.rect.x + 35*X
            s.beamRect.y = s.rect.y + 39*Y
            if s.fireingTime > 1000:
                if not s.laserSoundPlayed:
                    s.laserSound.play()
                    s.laserSoundPlayed = True
                s.beamFireing.time += deltaTime
                for i in range(ceil(pygame.display.Info().current_w/(21*X))+3):
                    s.beamFireing.update(screen, 0, (s.rect.x-i*s.beamRect.w + 35*X, s.beamRect.y))
            else:
                s.beamLoading.time += deltaTime
                for i in range(ceil(pygame.display.Info().current_w/(21*X))+3):
                    s.beamLoading.update(screen, 0, (s.rect.x-(i+1)*s.beamRect.w + 35*X, s.beamRect.y))
        else:
            if s.rect.x > pygame.display.Info().current_w*s.Xmax:
                if s.rect.y < ship.rect.y - 100*Y:
                    y = 0.5*deltaTime
                elif s.rect.y > ship.rect.y + 100*Y:
                    y = -0.5*deltaTime
                else:
                    s.fireing = True
                    
            else:
                x = 1.3*deltaTime

        for laserShip in laserShipGroup:
            if s.rect.colliderect(laserShip.rect) and not s.fireing:
                if laserShip.rect.y < s.rect.y and laserShip.rect.y + laserShip.rect.h > s.rect.y and laserShip.rect.y + laserShip.rect.h < s.rect.y + s.rect.h:
                    y = 0.5*deltaTime
                elif laserShip.rect.y + laserShip.rect.h > s.rect.y +s.rect.h and laserShip.rect.y > s.rect.y and laserShip.rect.y < s.rect.y + s.rect.h :
                    y = -0.5*deltaTime
                    
        s.rect.move_ip(x, y)
        s.anim.update(screen, deltaTime, s.rect)

class NuclearMissile(pygame.sprite.Sprite):        
    #créé les missiles uranium
    
    def __init__(s, posX, posY, animationImage): 
            
        pygame.sprite.Sprite.__init__(s)
        s.anim = Animation(animationImage, 520, 110, 152, 35, 4, 200)
        s.rect = s.anim.get_rect()
        s.lifeTime = 200
        s.whiteScreenTime = 100
        s.spawned = False
        s.cooldown = 0
        
    def Spawn(s, rect):

        s.spawned = True
        s.rect.x = rect.x
        s.rect.y = rect.y 
        
    def update(s, screen, deltaTime):

        s.cooldown -= deltaTime
        if s.cooldown > 600 and s.cooldown%100 > 90:
            screen.fill((255,255,255))
        if s.spawned:
            s.lifeTime -= deltaTime
            if s.lifeTime <= 0:
                s.spawned = False
            s.rect.move_ip(1.1*deltaTime, 0)
            s.anim.update(screen, deltaTime, s.rect)

        

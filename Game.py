import pygame 
from pygame.locals import *
import sys, os
from random import randint
from Functions import *
from Classes import *
from Animation import *
from Items import *
from math import log

class Game:

    def __init__(s):

        s.animationImage = LoadImage('animations.png', True)
        s.missileItemImage = LoadImage('missileItem.png', True)
        s.enemeyShipImage = LoadImage('meteorite.png', True)
        s.imageHeart = LoadImage('heart.png', True)
        s.shieldImage = LoadImage('shield.png',True)
        s.spaceImage = LoadImage('space.png')
        s.nuclearMissileItemImage = LoadImage('nuclearMissileItem.png', True)
        
        s.missileSound = pygame.mixer.Sound(os.path.join('data','missileSound.wav'))
        s.explosionSound = pygame.mixer.Sound(os.path.join('data','explosion.wav'))
        s.music = pygame.mixer.Sound(os.path.join('data','music.wav'))
        s.laserSound = pygame.mixer.Sound(os.path.join('data','laserSound.wav'))
        s.nuclearMissileSound = pygame.mixer.Sound(os.path.join('data','nuclearMissileSound.wav'))
        s.nuclearExplosionSound = pygame.mixer.Sound(os.path.join('data','nuclearExplosionSound.wav'))
        
        s.missileSound.set_volume(0.5)
        s.explosionSound.set_volume(0.5)
        s.music.set_volume(0)
        s.Reset()
        s.time = 1

    def Reset(s):

        #initialisation de la classe permettant le scrolling de l'arrière plan
        s.background = Background(s.spaceImage)
        
        #initialsistation du vaisseau(ship) et des groupe de missiles(missiles) et d'asteroides(enemys)
        s.ship = Ship(pygame.display.Info().current_w/10, pygame.display.Info().current_h/2, s.animationImage, s.imageHeart, s.missileItemImage )
        s.shield = Shield(s.shieldImage)
        s.nuclearMissile = NuclearMissile(s.ship.rect.x , s.ship.rect.y, s.animationImage)
        
        s.missiles = pygame.sprite.Group()
        s.enemys = pygame.sprite.Group()
        s.explosionGroup = pygame.sprite.Group()
        s.enemyMissileGroup = pygame.sprite.Group()
        s.laserShipGroup = pygame.sprite.Group()
        
        s.missileItem = MissileItem(s.missileItemImage)
        s.shieldItem = ShieldItem(s.shieldImage)
        s.nuclearMissileItem = NuclearMissileItem(s.nuclearMissileItemImage)
            
        s.timeBetweenShot = 0 #initialisation du temps entre chaque tir de missile
        
        s.score = 0
        s.bestScore = 0
        s.music.play(loops = -1)
        pygame.mixer.pause()
        
    def Run(s, screen, timer, cData, font):

        pygame.mouse.set_visible(0)
        pygame.mixer.unpause()
        timer.tick()
        
        while True:
            if s.time < 60000000 :
                with open("scoreAsteroid.txt", "r") as fichier:
                    s.bestScore = round(float(fichier.read()))
            elif s.time > 60000000 and s.time < 120000000 :
                with open("scoreMissile.txt", "r") as fichier:
                    s.bestScore = round(float(fichier.read()))
            elif s.time > 120000000 and s.time < 180000000 :
                with open("scoreLaserShip.txt", "r") as fichier:
                    s.bestScore = round(float(fichier.read()))
            elif s.time > 180000000 and s.time < 200000000 :
                with open("scoreHell.txt", "r") as fichier:
                    s.bestScore = round(float(fichier.read()))
            elif s.time > 200000000 :
                with open("score.txt", "r") as fichier:
                    s.bestScore = round(float(fichier.read()))
                
        
            deltaTime = timer.tick()
            s.score += deltaTime/10
            s.time += deltaTime

            #recuperation des informastion du clavier:
            GetControlersData(cData)
                
            #gestion du tir des missiles:
            if s.ship.ammunition >0:
                s.timeBetweenShot -= deltaTime
                if cData["SPACE"] and s.timeBetweenShot <= 0:
                    s.ship.ammunition -= 1
                    s.missileSound.play()
                    s.timeBetweenShot = 400
                    s.missiles.add(Missile(s.ship.rect.x + 120, s.ship.rect.y + 15, s.animationImage))

            #gestion du tir des missiles nucleaires 
            if s.ship.nuclearMissileActivated :
                if cData['ENTER']:
                    s.nuclearMissileSound.play()
                    s.nuclearMissile.Spawn(s.ship.rect)
                    s.ship.nuclearMissileActivated = False

            #gestion de l'explosion du missile nucleair
            if s.nuclearMissile.lifeTime <= 0:
                s.nuclearMissileSound.stop()
                for enemy in s.enemys:
                    s.explosionGroup.add(Explosion(enemy.rect, s.animationImage))
                    enemy.kill()
                    s.score += 100
                for enemyMissiles in s.enemyMissileGroup:
                    enemyMissiles.kill()
                    s.explosionGroup.add(Explosion(enemyMissiles.rect, s.animationImage))
                    s.score += 100
                for laserShip in s.laserShipGroup:
                    laserShip.kill()
                    s.explosionGroup.add(Explosion(laserShip.rect, s.animationImage))
                    s.score += 100
                s.nuclearExplosionSound.play()
                s.nuclearMissile.lifeTime = 200
                s.nuclearMissile.cooldown = 1000
                
            if s.nuclearMissile.cooldown < 0:
                #spawn des asteroides:
                if randint(0,round(700000/s.time)) == 0 and s.time < 60000000 :
                    s.enemys.add(Enemy(s.enemeyShipImage))
                elif randint(0,round(40000000000/s.time)) ==0 and (s.time > 180000000 and s.time < 200000000):
                    s.enemys.add(Enemy(s.enemeyShipImage))
                elif randint(0,round(50000000000/s.time)) ==0 and (s.time > 200000000 and s.time < 200060000):
                    s.enemys.add(Enemy(s.enemeyShipImage))
                elif randint(0,round(40000000000/s.time)) ==0 and s.time > 200160000 :
                    s.enemys.add(Enemy(s.enemeyShipImage))
                
                #spawn des missiles a tête chercheuse
                if randint(0,round(7000000000/s.time)) == 0 and (s.time > 60000000  and s.time < 120000000) :
                    s.enemyMissileGroup.add(EnemyMissile(s.animationImage))
                elif randint(0,round(100000000000/s.time)) == 0 and (s.time > 180000000 and s.time < 200000000) :
                    s.enemyMissileGroup.add(EnemyMissile(s.animationImage))
                elif randint(0,round(100000000000/s.time)) == 0 and (s.time > 200060000 and s.time < 200120000):
                    s.enemyMissileGroup.add(EnemyMissile(s.animationImage))
                elif randint(0,round(100000000000/s.time)) == 0 and s.time > 200160000:
                    s.enemyMissileGroup.add(EnemyMissile(s.animationImage))
                                                               

                #spawn des vaisseaux ennemis
                if randint(0,round(100000000000/s.time)) == 0 and (s.time > 120000000 and s.time < 180000000):
                    s.laserShipGroup.add(LaserShip( s.animationImage, s.laserSound))
                elif randint(0,round(300000000000/s.time)) == 0 and (s.time > 180000000 and s.time < 200000000):
                    s.laserShipGroup.add(LaserShip( s.animationImage, s.laserSound))
                elif randint(0,round(580000000000/s.time)) == 0 and s.time > 200120000:
                    s.laserShipGroup.add(LaserShip( s.animationImage, s.laserSound))

            #spawn de l'item missile
            if randint(0,round(8000)) == 0 and not s.missileItem.spawned:
                    s.missileItem.Spawn()

            #spawn de l'item missile nucléaire
            if not s.ship.nuclearMissileActivated and randint(0,round(9000)) == 0 and not s.nuclearMissileItem.spawned:
                    s.nuclearMissileItem.Spawn()
                        
            #spwan du bouclier
            if not s.ship.shieldActivated and not s.shieldItem.spawned and randint(0,round(12000)) == 0:
                    s.shieldItem.Spawn()
                
            #gestion du deplacement et des collisions entre missile, asteroides et vaiseau du joueur 
            for enemy in s.enemys:
                for missile in s.missiles:
                    if missile.rect.colliderect(enemy.rect): #teste la collision entre les missile et les asteroides
                        s.explosionGroup.add(Explosion(enemy.rect, s.animationImage, s.explosionSound))
                        missile.kill()
                        enemy.kill()
                        s.score += 100
                if s.ship.rect.colliderect(enemy.rect):#teste les collision entre le vaisseau du joueur et les asteroides
                    s.explosionGroup.add(Explosion(s.ship.rect, s.animationImage, s.explosionSound))
                    s.ship.Hit()
                    enemy.kill()
                        
            #gestion de la colision entre le vaisseau et les missiles             
            for enemyMissile in s.enemyMissileGroup:
                if enemyMissile.rect.colliderect(s.ship.rect):
                    enemyMissile.kill()
                    s.ship.Hit()
                    s.explosionGroup.add(Explosion(s.ship.rect, s.animationImage, s.explosionSound))

            #gestion de la colision entre les vaisseaux ennemis et le vaisseau
            for laserShip in s.laserShipGroup:
                if laserShip.rect.colliderect(s.ship.rect):
                    s.ship.Hit()
                    s.explosionGroup.add(Explosion(s.ship.rect, s.animationImage, s.explosionSound))
                    laserShip.life -= 1
                    if laserShip.life == 0:
                        laserShip.kill()
                        s.explosionGroup.add(Explosion(s.ship.rect, s.animationImage, s.explosionSound))
                if laserShip.beamCollide(s.ship.rect) and laserShip.fireingTime > 1000:
                    s.ship.Hit()
                    laserShip.fireingTime = 2001
                    s.explosionGroup.add(Explosion(laserShip.rect, s.animationImage, s.explosionSound))
                for missile in s.missiles:
                    if laserShip.rect.colliderect(missile.rect):
                        missile.kill()
                        laserShip.life -= 1
                        if laserShip.life == 0:
                            laserShip.kill()
                            s.explosionGroup.add(Explosion(laserShip.rect, s.animationImage, s.explosionSound))
                            
            #affichage et deplacement des entitées:            
            s.background.update(screen, deltaTime)
            s.laserShipGroup.update(screen, deltaTime, s.ship, s.laserShipGroup)
            s.ship.update(screen, deltaTime, cData)
            s.enemys.update(screen, deltaTime)
            s.enemyMissileGroup.update(screen, deltaTime, s.ship)
            s.missileItem.update(screen, deltaTime, s.ship)
            s.shieldItem.update(screen, deltaTime, s.ship)
            s.shield.update(screen,s.ship, s.shieldImage)
            s.missiles.update(screen, deltaTime)
            s.explosionGroup.update(screen, deltaTime)
            s.nuclearMissileItem.update(screen, deltaTime, s.ship)
            s.nuclearMissile.update(screen, deltaTime)

            #affichage du nombre de missiles restant
            screen.blit(s.missileItemImage, (pygame.display.Info().current_w/6, 0))
            ammunition_font = font.render("{}".format(s.ship.ammunition), True, (255,255,255))
            ammunition_rect = ammunition_font.get_rect(topleft=(pygame.display.Info().current_w/6 + s.missileItemImage.get_width(), 0))
            screen.blit(ammunition_font, ammunition_rect)

            #affichage de la possesioin du missile nucléaire
            if s.ship.nuclearMissileActivated:
                screen.blit(s.nuclearMissileItemImage, (pygame.display.Info().current_w/8, 0))
            
            #affichage du temps necessaire pour executer chaque tour de boucle
            delay_font = font.render("delay: {}".format(deltaTime), True, (255,255,255))
            delay_rect = delay_font.get_rect(bottomright=(pygame.display.Info().current_w, pygame.display.Info().current_h))
            screen.blit(delay_font, delay_rect)

            #affichage du nombre d'image par secondes
            fps = font.render("fps: {:.1f}".format(timer.get_fps()), True, (255,255,255))
            fps_rect = fps.get_rect(bottomright=(pygame.display.Info().current_w, pygame.display.Info().current_h - delay_rect.h))
            screen.blit(fps, fps_rect)

            #affichage du score
            score_font = font.render("SCORE: {}".format(round(s.score)), True, (255,255,255))
            screen.blit(score_font, (0, s.ship.heartRect.h))

            #affichage du meilleur score
            if s.time < 60000000 :
                bestScore_font = font.render("BEST SCORE LEVEL ASTEROID: {}".format(round(s.bestScore)),True, (255,255,255))
            elif s.time > 60000000 and s.time < 120000000 :
                bestScore_font = font.render("BEST SCORE LEVEL MISSILE: {}".format(round(s.bestScore)),True, (255,255,255))
            elif s.time > 120000000 and s.time < 180000000 :
                bestScore_font = font.render("BEST SCORE LEVEL LASER SHIP: {}".format(round(s.bestScore)),True, (255,255,255))
            elif s.time > 180000000 and s.time < 200000000 :
                bestScore_font = font.render("BEST SCORE LEVEL HELL: {}".format(round(s.bestScore)),True, (255,255,255))
            elif s.time > 200000000 :
                bestScore_font = font.render("BEST SCORE NORMAL MODE: {}".format(round(s.bestScore)),True, (255,255,255))

            screen.blit(bestScore_font, (0, (s.ship.heartRect.h)*2))

            if s.ship.life <= 0:
                pygame.time.delay(2000)
                pygame.mouse.set_visible(1)
                s.music.stop()
                return ['GameOverScreen', s.score ,s.time]

            if cData['ESCAPE']:
                pygame.mixer.pause()
                return ['Pause']
             
            pygame.display.flip()
            

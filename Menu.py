import pygame
from pygame.locals import *

from Button import *
from Functions import *

class MainMenu:

    def __init__(s):
        
        s.buttonLevelHell = Button(LoadImage('levelHell.png', True, 0, 0, 144, 167), LoadImage('levelHell.png', True, 144, 0, 144, 167), pygame.display.Info().current_w/4, pygame.display.Info().current_h/1.5)
        s.buttonLevelAsteroid = Button(LoadImage('levelAsteroid.png', True, 0, 0, 144, 167), LoadImage('levelAsteroid.png', True, 144, 0, 144, 167), pygame.display.Info().current_w/4, pygame.display.Info().current_h/4) 
        s.background = LoadImage('space.png')
        s.buttonLevelMissile = Button(LoadImage('levelMissile.png', True, 0, 0, 144, 167), LoadImage('levelMissile.png', True, 144, 0, 144, 167), pygame.display.Info().current_w/ 1.5, pygame.display.Info().current_h/4)
        s.buttonLevelLaserShip = Button(LoadImage('levelLaserShip.png', True, 0, 0, 144, 167), LoadImage('levelLaserShip.png', True, 144, 0, 144, 167), pygame.display.Info().current_w/ 1.5, pygame.display.Info().current_h/1.5)
        s.buttonPlay = Button(LoadImage('buttonPlay.png', True, 0, 0, 410, 130), LoadImage('buttonPlay.png', True, 410, 0, 410 ,130), pygame.display.Info().current_w/2.5, pygame.display.Info().current_h/2)
        s.spaceShipImage = LoadImage('SpaceShip.png', True)
        
    def Run(s, screen, cData, game):
        
        pygame.mouse.set_visible(1)
        
        while True:
            screen.blit (s.background, (0,0))
            screen.blit (s.spaceShipImage, (pygame.display.Info().current_w/3.2, 50*pygame.display.Info().current_h/1440))

            GetControlersData(cData)

            s.buttonLevelHell.update(screen, cData)
            s.buttonLevelAsteroid.update(screen, cData)
            s.buttonLevelMissile.update(screen, cData)
            s.buttonLevelLaserShip.update(screen, cData)
            s.buttonPlay.update(screen, cData)
            
            if s.buttonLevelHell.clicked == True:
                game.time = 180000001
                return ['GameReset']
            elif s.buttonLevelAsteroid.clicked == True:
                game.time = 1
                return ['GameReset']
            elif s.buttonLevelMissile.clicked == True:
                game.time = 60000001
                return ['GameReset']
            elif s.buttonLevelLaserShip.clicked == True:
                game.time = 120000001
                return ['GameReset']
            elif s.buttonPlay.clicked == True:
                game.time = 200000001
                return ['GameReset']
            
            pygame.display.flip()

    
class PauseMenu:

    def __init__(s):
        button = LoadImage('buttonResume.png', True)
        s.buttonResume = Button(button, LoadImage('buttonResumeClicked.png', True), pygame.display.Info().current_w/2 - (button.get_width()/2), pygame.display.Info().current_h/2 - (button.get_height()/2))
        s.buttonMainMenu = Button(LoadImage('buttonMainMenu.png', True, 0, 0, 800, 110), LoadImage('buttonMainMenu.png', True, 800, 0, 800, 110), s.buttonResume.rect.x , s.buttonResume.rect.y + s.buttonResume.rect.h + 50*pygame.display.Info().current_h/1440)
        s.buttonLeaveGame = Button(LoadImage('buttonLeaveGame.png', True, 0, 0, 900, 140), LoadImage('buttonLeaveGame.png', True, 900, 0, 900, 140),  s.buttonMainMenu.rect.x , s.buttonMainMenu.rect.y + s.buttonMainMenu.rect.h + 50*pygame.display.Info().current_h/1440)
        s.background = LoadImage('space.png')
        
    def Run(s, screen, cData):
        
        pygame.mouse.set_visible(1)
        
        while True:

            GetControlersData(cData)

            s.buttonResume.update(screen, cData)
            s.buttonMainMenu.update(screen, cData)
            s.buttonLeaveGame.update(screen, cData)

            if s.buttonResume.clicked:
                return ['Game']
            elif s.buttonMainMenu.clicked:
                return ['MainMenu']
            elif s.buttonLeaveGame.clicked:
                return ['Quit']
            pygame.display.flip()

class GameOver:
    
    def __init__(s):
        s.buttonTryAgain = Button(LoadImage('buttonTryAgain.png', True, 0, 0, 690, 140), LoadImage('buttonTryAgain.png', True, 690, 0, 690, 140), pygame.display.Info().current_w/3, pygame.display.Info().current_h/2)
        s.buttonMainMenu = Button(LoadImage('buttonMainMenu.png', True, 0, 0, 800, 110), LoadImage('buttonMainMenu.png', True, 800, 0, 800, 110), s.buttonTryAgain.rect.x, s.buttonTryAgain.rect.y + s.buttonTryAgain.rect.h + 50*pygame.display.Info().current_h/1440)
        s.buttonLeaveGame = Button(LoadImage('buttonLeaveGame.png', True, 0, 0, 900, 140), LoadImage('buttonLeaveGame.png', True, 900, 0, 900, 140), s.buttonTryAgain.rect.x, s.buttonMainMenu.rect.y + s.buttonMainMenu.rect.h + 50*pygame.display.Info().current_h/1440)
        s.spaceImage = LoadImage('space.png')
        

    def Run(s, screen, cData, font, score, time):

            #lecture du meilleur score
            if time < 60000000 :
                with open("scoreAsteroid.txt", "r") as fichier:
                    bestScore = round(float(fichier.read()))
            elif time > 60000000 and time < 120000000 :
                with open("scoreMissile.txt", "r") as fichier:
                    bestScore = round(float(fichier.read()))
            elif time > 120000000 and time < 180000000 :
                with open("scoreLaserShip.txt", "r") as fichier:
                    bestScore = round(float(fichier.read()))
            elif time > 180000000 and time < 200000000 :
                with open("scoreHell.txt", "r") as fichier:
                    bestScore = round(float(fichier.read()))
            elif time > 200000000 :
                with open("score.txt", "r") as fichier:
                    bestScore = round(float(fichier.read()))
                
            #enregistrement du score si le score obtenu est plus élevé que le meilleur score
            if score > bestScore and time > 200000000 :
                bestScore = round(score)
                with open("score.txt", "w") as fichier:
                    fichier.write(str(score))
            elif score > bestScore and time > 120000000 and time < 180000000 :
                bestScore = round(score)
                with open("scoreLaserShip.txt", "w") as fichier:
                    fichier.write(str(score))
            elif score > bestScore and time > 60000000 and time < 120000000 :
                bestScore = round(score)
                with open("scoreMissile.txt", "w") as fichier:
                    fichier.write(str(score))
            elif score > bestScore and time < 60000000 :
                bestScore = round(score)
                with open("scoreAsteroid.txt", "w") as fichier:
                    fichier.write(str(score))
            elif score > bestScore and time > 180000000 and time < 200000000 :
                bestScore = round(score)
                with open("scoreHell.txt", "w") as fichier:
                    fichier.write(str(score)) 

            #affichage du game over + score realisé

                    
            while True:
                
                screen.blit(s.spaceImage, (0,0))

                gameOver = font.render("GAME OVER", True, (255,0,0))
                gameOver_rect = gameOver.get_rect(midbottom=(pygame.display.Info().current_w/2, pygame.display.Info().current_h/3))
                screen.blit(gameOver, gameOver_rect)
                
                if time < 60000000 :
                   levelName = 'ASTEROID MODE'
                elif time > 60000000 and time < 120000000 :
                    levelName = 'MISSILE MODE'
                elif time > 120000000 and time < 180000000 :
                    levelName = 'LASER SHIP MODE'
                elif time > 180000000 and time < 200000000 :
                    levelName = 'HELL MODE'
                elif time > 200000000 :
                    levelName = 'NORMAL MODE'
                
                bestScore_font = font.render("Best score {}: {}".format(levelName, bestScore), True, (255,255,255))
                bestScore_font_rect = bestScore_font.get_rect(midtop=(pygame.display.Info().current_w/2, pygame.display.Info().current_h/3))
                screen.blit(bestScore_font, bestScore_font_rect)
                
                score_font = font.render("your score: {}".format(round(score)), True, (255,255,255))
                score_font_rect = score_font.get_rect(midtop=(pygame.display.Info().current_w/2, bestScore_font_rect.y + (bestScore_font_rect.h)))
                screen.blit(score_font, score_font_rect)

                GetControlersData(cData)

                s.buttonTryAgain.update(screen, cData)
                s.buttonMainMenu.update(screen, cData)
                s.buttonLeaveGame.update(screen, cData)

                if s.buttonTryAgain.clicked:
                    return ['GameReset']
                elif s.buttonMainMenu.clicked:
                    return ['MainMenu']
                elif s.buttonLeaveGame.clicked:
                    return ['Quit']
                    
                pygame.display.update()



    

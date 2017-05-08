import pygame 
from pygame.locals import *
from Functions import *
from Classes import *
from Game import *
from Menu import*

#initialise les modules de pygame et renvoie une erreur puis ferme le programme si les modules ne se sont pas chargés correctement
try:
    pygame.init()
except pygame.error:
    print("Erreur d'initialisation")
    sys.exit(0)  

#creation de la fenetre en plein ecran et des timers
screen = pygame.display.set_mode((0,0), FULLSCREEN | DOUBLEBUF | HWSURFACE )#cree une fenetre en plein ecran et a la resolution maximale de l'ecran
timer = pygame.time.Clock()#timer mesurer le temps entre chaque image
font = pygame.font.Font("data/arial.ttf", 30)#initialisiation de la police d'ecriture

pygame.mixer.set_num_channels(32)
pygame.mixer.fadeout(300)

#initialisation du dictionaire contennant les infos du clavier:
cData = {'Z':False,
        'S':False,
        'Q':False,
        'D':False,
        'SPACE':False,
        'ESCAPE':False,
        'ENTER':False,

        'MOUSEX': 0,
        'MOUSEY': 0,
        'LEFTBUTTON':False,
        'RIGHTBUTTON':False}

game = Game()
mainMenu = MainMenu()
pauseMenu = PauseMenu()
gameOver = GameOver()

scene = ['MainMenu']
while scene[0] != 'Quit':

    if scene[0] == 'MainMenu':
        scene = mainMenu.Run(screen, cData, game)
    elif scene[0] == 'Game' :
        scene = game.Run(screen, timer, cData, font)
    elif scene[0] == 'GameReset':
        game.Reset()
        scene = game.Run(screen, timer, cData, font)
    elif scene[0] == 'GameOverScreen':
        scene = gameOver.Run(screen, cData, font, scene[1], scene[2])
    elif scene[0] == 'Pause':
        scene = pauseMenu.Run(screen, cData)
    
    
pygame.quit()

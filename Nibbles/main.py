"""
Author: Guilherme David Branco
NIBBLE/SNAKE CLONE GAME to learn PYGAME
"""
import random
import sys
import pygame
import time
from pygame.locals import *


####CONSTANTS
##GAME
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_CENTER = WINDOW_WIDTH/2, WINDOW_HEIGHT/2
CELL_SIZE = 25
CELL_WIDTH = int(WINDOW_WIDTH/CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT/CELL_SIZE)

##COLORS
COLORS = {
    'white':      (255, 255, 255),
    'black':      (0, 0, 0),
    'red':        (255, 0, 0),
    'green':      (0, 255, 0),
    'blue':       (0, 0, 255),
    'dark_green': (0, 155, 0),
    'dark_gray':  (40, 40, 40),
}
BGCOLOR = COLORS['black']
##MOVEMENT
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
##SNAKE HEAD
HEAD = 0
DIRECTION = None
APPLE = None
WORM = None
SCORE = 0
def endGame():
    pygame.quit()
    sys.exit()

def checkKeyPress():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        endGame()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        endGame()
    pygame.event.get()
    return keyUpEvents[0].key
def clearScreen():
    DISPLAYSURF.fill(BGCOLOR)

def drawPressKey(inverte):
    pressFont = pygame.font.Font('./waffle.otf', 30)
    pressKeySurf = pressFont.render('Pressione qualquer botão para começar',
                                    True, COLORS['green'] if inverte else COLORS['black'])
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.x = WINDOW_WIDTH/2 - pressKeyRect.width/2
    pressKeyRect.y = WINDOW_HEIGHT/2 - pressKeyRect.height/2 + 100
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def showGameOver():
    print("GAMEOVER SCREEN")
    titleFont = pygame.font.Font("./waffle.otf", 100)
    titleSurf = titleFont.render('GAME OVER', True, COLORS['red'])
    titleRect = titleSurf.get_rect()
    X = 0 - titleRect.width
    Y = WINDOW_HEIGHT/2 - titleRect.height/2
    inverte = False
    while True:
        clearScreen()
        DISPLAYSURF.blit(titleSurf, (X, Y))
        drawPressKey(inverte)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        if X > (WINDOW_WIDTH + titleRect.width/2):
            X = -titleRect.width
        X += 15
        if X % 8 == 0:
            inverte = not inverte
        if checkKeyPress():
            resetGame()
            return

def showStart():
    print("START SCREEN")
    titleFont = pygame.font.Font("./waffle.otf", 100)
    titleSurf = titleFont.render('Snake Clone', True, COLORS['white'])
    titleRect = titleSurf.get_rect()
    X = 0 - titleRect.width
    Y = WINDOW_HEIGHT/2 - titleRect.height/2
    inverte = False
    while True:
        clearScreen()
        DISPLAYSURF.blit(titleSurf, (X, Y))
        drawPressKey(inverte)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        if X > (WINDOW_WIDTH + titleRect.width/2):
            X = -titleRect.width
        X += 15
        if X % 8 == 0:
            inverte = not inverte
        if checkKeyPress():
            return

def getRandomLocation():
    x = random.randint(0, CELL_SIZE - 1)
    y = random.randint(0, CELL_SIZE - 1)
    return [x, y]

def handleEvents():
    global DIRECTION
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endGame()
            elif event.type == KEYDOWN:
                if(event.key == K_LEFT or event.key == K_a) and DIRECTION != RIGHT:
                    DIRECTION = LEFT
                elif(event.key == K_RIGHT or event.key == K_d) and DIRECTION != LEFT:
                    DIRECTION = RIGHT
                elif(event.key == K_UP or event.key == K_w) and DIRECTION != DOWN:
                    DIRECTION = UP
                elif(event.key == K_DOWN or event.key == K_s) and DIRECTION != UP:
                    DIRECTION = DOWN
def drawGrid():
    for x in range(0, WINDOW_WIDTH, CELL_WIDTH):
        pygame.draw.line(DISPLAYSURF, COLORS['white'], (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_HEIGHT):
        pygame.draw.line(DISPLAYSURF, COLORS['white'], (0, y), (WINDOW_WIDTH, y))
def resetGame():
    global DIRECTION
    global APPLE
    global WORM
    APPLE = getRandomLocation()
    WORM = []
    WORM.insert(0,getRandomLocation())
    clearScreen()
    DIRECTION = None
def runGame():
    global DIRECTION
    global APPLE
    global WORM
    print("RUNNING GAME")
    resetGame()
    while True:
        clearScreen()
        handleEvents()
        # drawGrid()
        moveWORM(WORM)
        if checkEating(WORM,APPLE):
            APPLE = getRandomLocation()
        else:
            del WORM[-1]
        if checkBounds(WORM):
            showGameOver()
        drawAPPLE(APPLE)
        drawWORM(WORM)
        pygame.display.update()
        FPSCLOCK.tick(FPS/6)

def moveWORM(WORM):
    global DIRECTION
    if DIRECTION == UP:
        newHead = [WORM[HEAD][0], WORM[HEAD][1] - 1]
    elif DIRECTION == DOWN:
        newHead = [WORM[HEAD][0], WORM[HEAD][1] + 1]
    elif DIRECTION == LEFT:
        newHead = [WORM[HEAD][0] - 1, WORM[HEAD][1]]
    elif DIRECTION == RIGHT:
        newHead = [WORM[HEAD][0] + 1, WORM[HEAD][1]]
    elif DIRECTION is None:
        newHead = [WORM[HEAD][0], WORM[HEAD][1]]
    WORM.insert(0, newHead)

def checkEating(WORM, APPLE):
    if WORM[HEAD][0] == APPLE[0] and WORM[HEAD][1] == APPLE[1]:
        return True
    return False

def checkBounds(WORM):
    if WORM[HEAD][0] < 0 or WORM[HEAD][0] > CELL_SIZE - 1 or WORM[HEAD][1] < 0 or WORM[HEAD][1] > CELL_SIZE - 1:
        return True
    for segment in WORM[1:]:
        if segment[0] == WORM[HEAD][0] and segment[1] == WORM[HEAD][1]:
            return True
    return False

def drawWORM(WORM):
    for coord in WORM:
        x = coord[0]*CELL_WIDTH
        y = coord[1]*CELL_HEIGHT
        WORMRect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
        pygame.draw.rect(DISPLAYSURF, COLORS['dark_green'], WORMRect)
        WORMInnerRect = pygame.Rect(x + 4, y + 4, CELL_WIDTH - 8, CELL_HEIGHT - 8)
        pygame.draw.rect(DISPLAYSURF, COLORS['green'], WORMInnerRect)

def drawAPPLE(coord):
    APPLERect = pygame.Rect(coord[0]*CELL_WIDTH,coord[1]*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
    pygame.draw.rect(DISPLAYSURF, COLORS['red'], APPLERect)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('SNAKE CLONE')
    showStart()
    while True:
        runGame()

if __name__ == "__main__":
    main()


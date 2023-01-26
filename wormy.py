# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys,math
from pygame.locals import *

FPS = 5
CELLSIZE = 20
WINDOWWIDTH = 40 * CELLSIZE
WINDOWHEIGHT = 30 * CELLSIZE
RADIUS = math.floor(CELLSIZE/2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
APPLECOUNT = 2
WORMCOUNT = 2

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
PURPLE    = (153,   0, 153)
PINK      = (204,   0, 102)
YELLOW = (255,255,0)
BGCOLOR = BLACK

WORMCOLORS = [[DARKGREEN, GREEN], [PURPLE, PINK]]

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snek knock off')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = []
    starty = []
    wormCoords = []
    direction = []
    ateApple = []
    isDead = []
    appleList = []
    stoneList = []
    isLaserRend = [False, False]
    sliceWormList = []

    for i in range(WORMCOUNT):
        startx.append(random.randint(5, CELLWIDTH - 6))
        starty.append(random.randint(5, CELLHEIGHT - 6))

        wormCoords.append( [{'x': startx[i],     'y': starty[i]},
                            {'x': startx[i] - 1, 'y': starty[i]},
                            {'x': startx[i] - 2, 'y': starty[i]}])
        direction.append(RIGHT)
        ateApple.append(False)
        isDead.append(False)


    # Start the apple in a random place.
    for i in range(APPLECOUNT):
        appleList.append(getRandomLocation())
    # apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction[0] != RIGHT:
                    direction[0] = LEFT
                elif (event.key == K_a) and direction[1] != RIGHT:
                    direction[1] = LEFT
                elif event.key == K_KP4:
                    for i in range(WORMCOUNT):
                        if direction[i] != RIGHT:
                            direction[i] = LEFT

                elif (event.key == K_RIGHT) and direction[0] != LEFT:
                    direction[0] = RIGHT
                elif (event.key == K_d) and direction[1] != LEFT:
                    direction[1] = RIGHT
                elif event.key == K_KP6:
                    for i in range(WORMCOUNT):
                        if direction[i] != LEFT:
                            direction[i] = RIGHT

                elif (event.key == K_UP) and direction[0] != DOWN:
                    direction[0] = UP
                elif (event.key == K_w) and direction[1] != DOWN:
                    direction[1] = UP
                elif event.key == K_KP8:
                    for i in range(WORMCOUNT):
                        if direction[i] != DOWN:
                            direction[i] = UP

                elif (event.key == K_DOWN) and direction[0] != UP:
                    direction[0] = DOWN
                elif (event.key == K_s) and direction[1] != UP:
                    direction[1] = DOWN
                elif event.key == K_KP2:
                    for i in range(WORMCOUNT):
                        if direction[i] != UP:
                            direction[i] = DOWN

                elif event.key == K_m: # player 0 laser
                    isLaserRend[0] = True
                    headSec = wormCoords[0][HEAD]
                    targetSec = wormCoords[1][0]

                    if(direction[0] == UP):
                        for i in range(len(wormCoords[1])):
                            targetSec = wormCoords[1][i]
                            if (targetSec['y'] >= headSec['y']) and targetSec['x'] == headSec['x']:
                                stoneList += wormCoords[1][i:]
                                del wormCoords[1][i:]
                                break
                    elif(direction[0] == RIGHT):
                        for i in range(len(wormCoords[1])):
                            targetSec = wormCoords[1][i]
                            if (targetSec['x'] >= headSec['x']) and targetSec['y'] == headSec['y']:
                                stoneList += wormCoords[1][i:]
                                del wormCoords[1][i:]
                                break

                    elif(direction[0] == DOWN):
                        for i in range(len(wormCoords[1])):
                            targetSec = wormCoords[1][i]
                            if (targetSec['y'] <= headSec['y']) and targetSec['x'] == headSec['x']:
                                stoneList += wormCoords[1][i:]
                                del wormCoords[1][i:]
                                break

                    elif(direction[0] == LEFT):
                        for i in range(len(wormCoords[1])):
                            targetSec = wormCoords[1][i]
                            if (targetSec['x'] <= headSec['x']) and targetSec['y'] == headSec['y']:
                                stoneList += wormCoords[1][i:]
                                del wormCoords[1][i:]
                                break


                elif event.key == K_q: # player 1 laser
                    isLaserRend[1] = True
                    headSec = wormCoords[1][HEAD]
                    targetSec = wormCoords[0][0] # target worm 0

                    if(direction[1] == UP):
                        for i in range(len(wormCoords[0])):
                            targetSec = wormCoords[0][i]
                            if (targetSec['y'] >= headSec['y']) and targetSec['x'] == headSec['x']:
                                stoneList += wormCoords[0][i:]
                                del wormCoords[0][i:]
                                break
                    elif(direction[1] == RIGHT):
                        for i in range(len(wormCoords[0])):
                            targetSec = wormCoords[0][i]
                            if (targetSec['x'] >= headSec['x']) and targetSec['y'] == headSec['y']:
                                stoneList += wormCoords[0][i:]
                                del wormCoords[0][i:]
                                break

                    elif(direction[1] == DOWN):
                        for i in range(len(wormCoords[0])):
                            targetSec = wormCoords[0][i]
                            if (targetSec['y'] <= headSec['y']) and targetSec['x'] == headSec['x']:
                                stoneList += wormCoords[0][i:]
                                del wormCoords[0][i:]
                                break

                    elif(direction[1] == LEFT):
                        for i in range(len(wormCoords[0])):
                            targetSec = wormCoords[0][i]
                            if (targetSec['x'] <= headSec['x']) and targetSec['y'] == headSec['y']:
                                stoneList += wormCoords[0][i:]
                                del wormCoords[0][i:]
                                break


                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        for i in range(WORMCOUNT):
            if isDead[i]:
                continue
            if wormCoords[i][HEAD]['x'] == -1 or wormCoords[i][HEAD]['x'] == CELLWIDTH or wormCoords[i][HEAD]['y'] == -1 or wormCoords[i][HEAD]['y'] == CELLHEIGHT:
                isDead[i] = True # game over for that worm
                for coord in wormCoords[i]:
                    stoneList.append(coord)
                continue
            for worm in wormCoords:
                for wormBody in worm[1:]:
                    if wormBody['x'] == wormCoords[i][HEAD]['x'] and wormBody['y'] == wormCoords[i][HEAD]['y']:
                        isDead[i] = True # game over for that worm
                        for coord in wormCoords[i]:
                            stoneList.append(coord)
                        continue

        if isDead[0] and isDead[1]:
            return # game over for all


        # check if worm has eaten an apple
        for i in range(APPLECOUNT):
            for j in range(WORMCOUNT):
                if wormCoords[j][HEAD]['x'] == appleList[i]['x'] and wormCoords[j][HEAD]['y'] == appleList[i]['y']:
                    # don't remove worm's tail segment
                    appleList[i] = getRandomLocation() # set a new apple somewhere
                    ateApple[j] = True

        for i in range(WORMCOUNT):
            if not ateApple[i] and not isDead[i]:
                del wormCoords[i][-1] # remove worm's tail segment
            ateApple[i] = False

        # move the worm by adding a segment in the direction it is moving
        for i in range(WORMCOUNT):
            if isDead[i]:
                continue
            if direction[i] == UP:
                newHead = {'x': wormCoords[i][HEAD]['x'], 'y': wormCoords[i][HEAD]['y'] - 1}
            elif direction[i] == DOWN:
                newHead = {'x': wormCoords[i][HEAD]['x'], 'y': wormCoords[i][HEAD]['y'] + 1}
            elif direction[i] == LEFT:
                newHead = {'x': wormCoords[i][HEAD]['x'] - 1, 'y': wormCoords[i][HEAD]['y']}
            elif direction[i] == RIGHT:
                newHead = {'x': wormCoords[i][HEAD]['x'] + 1, 'y': wormCoords[i][HEAD]['y']}
            wormCoords[i].insert(0, newHead)   #have already removed the last segment

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()

        for i in range(WORMCOUNT):
            drawWorm(wormCoords[i], i)

        drawStones(stoneList)

        for apple in appleList:
            drawApple(apple)

        for i in range(WORMCOUNT):
            drawScore(len(wormCoords[i]) - 3, i)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, YELLOW)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Many', True, BLACK, PURPLE)
    titleSurf2 = titleFont.render('Snek', True, PINK)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)
    overRect.midtop = (math.floor(WINDOWWIDTH / 2), gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score, offset):
    scoreSurf = BASICFONT.render(f"Score {offset + 1}: {score}", True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (30, 10 + (offset * 50))
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, wormNum):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, WORMCOLORS[wormNum][0], wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WORMCOLORS[wormNum][1], wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    xcenter = coord['x'] * CELLSIZE + math.floor(CELLSIZE/2)
    ycenter = coord['y'] * CELLSIZE+ math.floor(CELLSIZE/2)
    #appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    #pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    pygame.draw.circle(DISPLAYSURF, RED,(xcenter,ycenter),RADIUS)


def drawStones(stones):
    for coord in stones:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormInnerSegmentRect)


def drawLaser(wormHead, direction):
    # loop from start (wormHead + 1)
    x = wormHead['x']
    y = wormHead['y']
    if direction == UP:
        # x stays same, y increases
        # start the laser one above the head, y + 1
        laserX = x * CELLSIZE
        for newY in range(y + 1, CELLHEIGHT):
            # draw the cells for the red line
            laserY = newY * CELLSIZE
            laserLineRect = pygame.Rect(laserX, laserY, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, RED, laserLineRect)
    elif direction == DOWN:
        # x stays the same, y decreases
        # start laser at edge and end below the head, (range does not include upper bound)
        laserX = x * CELLSIZE
        for newY in range(0, y):
            # draw the cells for the red line
            laserY = newY * CELLSIZE
            laserLineRect = pygame.Rect(laserX, laserY, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, RED, laserLineRect)
    elif direction == LEFT:
        # y stays the same, x decreases
        # start laser at edge and end before the head, (range does not include upper bound)
        laserY = y * CELLSIZE
        for newX in range(0, x):
            # draw the cells for the red line
            laserX = newX * CELLSIZE
            laserLineRect = pygame.Rect(laserX, laserY, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, RED, laserLineRect)
    elif direction == RIGHT:
        # y stays the same, x increases
        # start laser one after head and end at edge
        laserY = y * CELLSIZE
        for newX in range(x + 1, CELLWIDTH):
            # draw the cells for the red line
            laserX = newX * CELLSIZE
            laserLineRect = pygame.Rect(laserX, laserY, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, RED, laserLineRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
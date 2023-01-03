# Bismillah Rahman Rahim
import math
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_icon(pygame.image.load('img/icon.png'))
pygame.display.set_caption('Jr board game')
# music
mixer.music.load('music/ES_Smoke Signal - Dust Follows.mp3')
mixer.music.play(-1)
# Player
playerX = 370
playerY = 500
playerX_change = 0


def player(x, y):
    screen.blit(pygame.image.load('img/board.png'), (x, y))


# ball
ballX = playerX
ballY = 480
ballX_change = 0
ballY_change = 30
ball_status = 'ready'


def ball(x, y):
    global ball_status
    ball_status = 'fire'
    screen.blit(pygame.image.load('img/ball.png'), (x + 20, y + 16))


# Life
life = 2

scr = 0
font = pygame.font.Font('freesansbold.ttf', 16)


def playerLife():
    screen.blit(font.render("Life:", True, (255, 255, 255)), (650, 500))
    x = 40
    for elem in range(life + 1):
        screen.blit(pygame.image.load('img/ball.png'), (650 + x, 500))
        x += 30


# wood goal
woodX = [[]]
woodY = [[]]
woodImg = [[]]


def Reset():
    global woodX
    global woodY
    global woodImg
    woodX = [[]]
    woodY = [[]]
    woodImg = [[]]
    coordinateX = 0
    coordinateY = 0
    j = 0
    for i in range(48):
        if i % 12 == 0 and i != 0:
            coordinateY += 40
            coordinateX = 0
            woodX.append([])
            woodY.append([])
            woodImg.append([])
            j += 1
        woodX[j].append(coordinateX)
        woodY[j].append(coordinateY)
        woodImg[j].append(pygame.image.load('img/wood.png'))
        coordinateX += 67


Reset()


def wood(x, y):
    screen.blit(woodImg[col][row], (x, y))


# Time
time = 0


def gettingHard():
    for i in range(len(woodY)):
        for j in range(len(woodY[i])):
            woodY[i][j] += 30


# Collision for wood
def Iscollision(woodX, woodY, ballX, ballY):
    distance = True if math.sqrt(math.pow((woodX - ballX), 2) + math.pow((woodY - ballY), 2)) < 35 else False
    return distance


# Collision for skateboard
def IscollisonSkate(playerX, playerY, ballX, ballY):
    global ballX_change
    distance = math.sqrt(math.pow((playerX - ballX), 2) + math.pow((playerY - ballY), 2))
    if distance < 35:
        return True
    elif distance < 42:
        if (playerX - ballX) < 0:
            ballX_change = -5
        else:
            ballX_change = 5
        return True
    else:
        return False


# checking the game
def Islevel():
    for i in woodY:
        for j in i:
            if j != 2000:
                return False
    else:
        return True


# Score
scr = 0
font = pygame.font.Font('freesansbold.ttf', 16)


def Textscore():
    screen.blit(font.render("Score: " + str(scr), True, (255, 255, 255)), (4, 500))


# game over
game_over_text = pygame.font.Font('freesansbold.ttf', 64)

game_over_bool = True


def GameOver():
    global game_over_bool
    screen.blit(game_over_text.render("GAME OVER", True, (255, 255, 255)), (200, 250))
    game_over_bool = False


# level
level = 1

font_level = pygame.font.Font('freesansbold.ttf', 16)


def LevelText():
    screen.blit(font_level.render("Level: " + str(level), True, (255, 255, 255)), (4, 530))


# restart
def init_game():
    global woodX, woodY, woodImg, level, scr, life
    woodX = [[]]
    woodY = [[]]
    woodImg = [[]]
    level = 1
    scr = 0
    life = 2
    Reset()


# running process
run = True
while run:
    col = 0
    row = 0
    screen.blit(pygame.image.load('img/back-ground.jpg'), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -30
            elif event.key == pygame.K_RIGHT:
                playerX_change = 30

            if event.key == pygame.K_SPACE:
                if ball_status is 'ready' and game_over_bool:
                    ballX = playerX
                    ball(ballX, ballY)
            if event.key == pygame.K_RETURN:
                init_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if ballY <= -1:
        ballY_change = -ballY_change
    elif ballY >= 480 and ballY_change < 0:
        if IscollisonSkate(playerX, playerY, ballX, ballY):
            ballY_change = -ballY_change
#            mixer.Sound('music/bat+hit+ball.wav').play()
        else:
            if life <= 0:
                GameOver()
                life = -1
            else:
                life -= 1
                ball_status = 'ready'
                ballX = playerX
                ballY = 480

    if ballX <= 0:
        ballX_change = -ballX_change
    elif ballX >= 736:
        ballX_change = -ballX_change

    if ball_status is 'fire':
        ball(ballX, ballY)
        ballY -= ballY_change
        ballX -= ballX_change

    for i in range(48):
        if i % 12 == 0 and i != 0:
            col += 1
            row = 0
        if Iscollision(woodX[col][row], woodY[col][row], ballX, ballY):
            woodY[col][row] = 2000
 #           mixer.Sound('music/Branch Wood Stress Cracking-SoundBible.com-2062541157.wav').play()
            ballY_change = -ballY_change
            scr += 1
        wood(woodX[col][row], woodY[col][row])
        row += 1

    if Islevel():
        Reset()
        level += 1

    # doing hard
    if (pygame.time.get_ticks() - time) / level > 30000:
        time = pygame.time.get_ticks()
        gettingHard()

    for elem in range(len(woodY)):
        if 480 in woodY[elem]:
            GameOver()
            life = 0

    Textscore()
    LevelText()
    playerLife()
    player(playerX, playerY)
    pygame.display.update()


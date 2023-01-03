import pygame
import random
import math
from pygame import mixer

# initialization of pygame
pygame.init()

# opening window of pygame
screen = pygame.display.set_mode((800, 600))

# getting img
icon = pygame.image.load('icons/ufo.png')

# inputting icon
pygame.display.set_icon(icon)

# Getting title for our game
pygame.display.set_caption('Nazirov Game')

# background music
mixer.music.load('music/background.wav')
mixer.music.play(-1)
# putting coordination of racket
playerX = 370
playerY = 480

# element for moving our racket
playerX_change = 0
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyImg = []
for i in range(6):
    # getting coordination of enemy
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(20, 120))

    # for changing coordination of enemy
    enemyX_change.append(4)
    enemyY_change.append(30)
    enemyImg.append(pygame.image.load('img/enemy.png'))
# getting coordination of enemy
bulletY = 480
bulletX = 0
# for changing coordination of enemy
bulletY_change = 10
# for checking can we fire
bullet_status = 'ready'

# for counting score of game
score = 0

# adding font
font = pygame.font.Font('freesansbold.ttf', 24)

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


# showing in screen score
def score_result():
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


# showing game over text
def game_over():
    game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


# Inputting our img racket in window
def playerImg(x, y):
    screen.blit(pygame.image.load('img/spaceship.png'), (x, y))


# Inputting our img enemy in window
def enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y))


# Inputting our img bullet in window
def bulletFire(x, y):
    global bullet_status
    bullet_status = 'fire'
    screen.blit(pygame.image.load('img/bullet.png'), (x + 16, y + 10))


# we checking if bullet and enemy coordinate is near we kill it
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = True if math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)) < 27 else False
    return distance


# this is operation doing for not closing the window
running = True
while running:
    # filling back-ground of our game in white color
    screen.fill((255, 255, 255))
    # Inputting background photo
    screen.blit(pygame.image.load('img/background.png'), (0, 0))
    # getting all event which happening in window or screen
    for event in pygame.event.get():

        # if we click in x the program will close
        if event.type == pygame.QUIT:
            running = False

        # we moving racket  on onclick in kleft or kright
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_status is 'ready':
                    mixer.Sound('music/laser.wav').play()
                    bulletX = playerX
                    bulletFire(bulletX, bulletY)

        # we stopping moving the racket
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # if racket getting edge of window stop increasing or decreasing the value of coordinate
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if bulletY <= 0:
        bulletY = 480
        bullet_status = 'ready'
    # for moving bullet
    if bullet_status is 'fire':
        bulletFire(bulletX, bulletY)
        bulletY -= bulletY_change

    playerImg(playerX, playerY)

    for i in range(6):
        if enemyY[i] > 460:
            game_over()
            for j in range(6):
                enemyY[j] = 2000
            score_result()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = 480
            bullet_status = 'ready'
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(20, 120)
            mixer.Sound('music/explosion.wav').play()
            score += 1
        score_result()
        enemy(enemyX[i], enemyY[i], i)
    # updating screen of game
    pygame.display.update()

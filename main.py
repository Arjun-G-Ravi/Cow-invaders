import pygame
import random
import math
import time

pygame.init()

# Screen
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Cow invaders")
running = True
# pygame.display.set_icon(pygame.image.load('10_Pygame learn/01_Space Invaders /spaceship.png')) # wont wprk in ubuntu

# bgm
pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)
# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 40)

def show_score():
    render = font.render("Score: "+str(score), True, (255,255,255))
    screen.blit(render, (10,10))

# Cow
playerImg = pygame.image.load('./cow.png')
player_pos = [400,500]
go_left = False
go_right = False

def player(x,y):
    screen.blit(playerImg, player_pos)

# Enemy
enemyImg = []
enemyPos = []
num_enemy = 3
horizontal_motion = [random.randint(1,5) for i in range(num_enemy)]
vertical_motion = [1 for i in range(num_enemy)]

for i in range(num_enemy):
    enemyimg = pygame.image.load('monster1.png')
    enemypos = [random.randint(100, 700), random.randint(0, 200)]
    enemyImg.append(enemyimg)
    enemyPos.append(enemypos)

def enemy(enemyImg, enemypos):
    screen.blit(enemyImg, enemypos)
       
def createEnemy(ch): # img, pos, horiz_motion, vertical motion
    global enemyImg
    global enemyPos
    global vertical_motion
    global horizontal_motion
    global num_enemy
    num_enemy += 1
    monster_type = {1:['monster1.png', [random.randint(100, 700), random.randint(0, 200)], random.randint(1,5), .75],
                    2:['monster2.png', [random.randint(100, 700), random.randint(0, 50)], random.randint(5,15), .5],
                    3:['monster3.png', [random.randint(100, 700), random.randint(0, 50)], random.randint(5,7), 2] }
    enemyImg.append(pygame.image.load(monster_type[ch][0]))
    enemyPos.append(monster_type[ch][1])
    horizontal_motion.append(monster_type[ch][2])
    vertical_motion.append(monster_type[ch][3])
    
# Milk
milkImg = pygame.image.load('milk-bottle.png')
milkPos = [480,500]
fire = False
milkSpeed = 20

def shoot_milk(milkPos):
    global fire
    fire = True
    milk = pygame.mixer.Sound('laser.wav')
    milk.play()
    

# Collision detection
def isCollision(pos1, pos2, distance=27):
    dis = math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
    if dis < distance:
        return True
    return False

# main loop
while running:
    
    # fill screen with grass image
    screen.blit(pygame.image.load('grass_background.png'),(0,0))
    show_score()
 
    for event in pygame.event.get(): 
        # print(event)               
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                go_left = True
                go_right = False 
    
            if event.key == pygame.K_RIGHT:
                go_right = True
                go_left = False
                
            if event.key == pygame.K_SPACE:
                if not fire:
                    milkPos[0] = player_pos[0]
                    shoot_milk(milkPos)
            
            if event.key == pygame.K_ESCAPE:
                print('cow')
                pause = True
                
        if event.type == pygame.KEYUP:
            go_left = False
            go_right = False
    
    if go_left:
        if player_pos[0] > 20:
            player_pos[0] -= 10
    
    if go_right:
        if player_pos[0] < 720:
            player_pos[0] += 10
    
    # For each enemy in list
    for e in range(num_enemy):
        enemy(enemyImg[e], enemyPos[e])
        if enemyPos[e][0] < 20:
            horizontal_motion[e] = - horizontal_motion[e]
            
        elif enemyPos[e][0] > 750:
            horizontal_motion[e] = - horizontal_motion[e]
       
        enemyPos[e][0] += horizontal_motion[e]
        enemyPos[e][1] += vertical_motion[e]
        
        if isCollision(milkPos, enemyPos[e]):
            screen.blit(pygame.image.load('explode.png'), enemyPos[e])
            enemyPos[e] = [random.randint(100, 700), random.randint(0, 100)]
            fire = False
            milkPos[1] = 500
            score += 1
            rand = random.randint(1,500)
            if rand <= 50: # 10%
                createEnemy(1)
            elif rand <= 55: # 1%
                createEnemy(2)
            elif rand <= 56: # 0.2%
                createEnemy(3)
            else:
                pass
            milk = pygame.mixer.Sound('grunt.mp3')
            milk.play()

        if enemyPos[e][1] > 600:
            milk = pygame.mixer.Sound('evil_laugh.mp3')
            milk.play()
            screen.blit(pygame.image.load('grass_background.png'),(0,0))
            screen.blit(pygame.image.load('spooky.png'), (enemyPos[e][0]-20, enemyPos[e][1]-80))
            while True:
                endFont1 = pygame.font.Font('freesansbold.ttf', 80)
                endFont2 = pygame.font.Font('freesansbold.ttf', 60)
                endFont3 = pygame.font.Font('freesansbold.ttf', 30)
                gameOver = endFont1.render("GAME OVER", True, (255,255,255))
                finalScore = endFont2.render("TOTAL SCORE: "+str(score), True, (255,255,255))
                press = endFont3.render("Press any key to quit.", True, (255,255,255))
                screen.blit(gameOver, (150,250))
                screen.blit(finalScore, (150,100))
                screen.blit(press, (240,350))
                pygame.display.update() 
                time.sleep(1)
                for event in pygame.event.get():  
                    if event.type == pygame.KEYDOWN:
                        quit(0)

        if isCollision(player_pos, enemyPos[e], 40): # Cow kills, but it increases enemy spawn rate by 2 times !!!
            screen.blit(pygame.image.load('explode.png'), enemyPos[e])
            enemyPos[e] = [random.randint(100, 700), random.randint(0, 100)]
            score += 1
            rand = random.randint(1,500)
            
            if rand <= 100: # 20%
                createEnemy(1)
            elif rand <= 110: # 2%
                createEnemy(2)
            elif rand <= 112: # 0.4%
                createEnemy(3)
            else:
                pass
            milk = pygame.mixer.Sound('grunt.mp3')
            milk.play()
            milk = pygame.mixer.Sound('moo.wav')
            milk.play()
                         
    # place player(cow) at player_pos
    player(player_pos[0], player_pos[1])

    # fire milk
    if fire:
        screen.blit(milkImg, milkPos)
        if milkPos[1] == 500:
            milkPos[0] = player_pos[0]
        milkPos[1] -= milkSpeed
        if milkPos[1] <= 0:
            fire = False
            milkPos[1] = 500

    # This is where the screen gets updated with the above changes
    pygame.display.update()

    # A clock adjusts frame rate
    pygame.time.Clock().tick(60)
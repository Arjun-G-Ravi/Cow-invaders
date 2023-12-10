# imports
import pygame
import random
import math
import time

# Initialisations
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Cow invaders")
running = True
pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 40)
smallFont = pygame.font.Font('freesansbold.ttf', 14)

def show_score():
    render = font.render("Score: "+ str(score), True, (255,255,255))
    screen.blit(render, (10,10))

# Cow
playerImg = pygame.image.load('./cow.png')
player_pos = [400,500]
go_left = False
go_right = False
cow_speed = 5
jump = False
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

# upgrades
upgrade = 0

def enable_upgrades(upgrade):
    if upgrade >= 1:
        # Cow speed up
        global cow_speed
        cow_speed = 10
        render = smallFont.render("Upgrade Unlocked: Faster Cow", True, (255,255,255))
        screen.blit(render, (10,50))
    
    if upgrade >= 2:
        # cow jump
        render = smallFont.render("Upgrade Unlocked: Cow jump", True, (255,255,255))
        screen.blit(render, (10,70))
    
    if upgrade >= 3:
        # Faster bullet
        global milkSpeed 
        milkSpeed = 40
        render = smallFont.render("Upgrade Unlocked: Faster Bullet", True, (255,255,255))
        screen.blit(render, (10,90))
        
    if upgrade >= 4:
        # pass through bullet
        render = smallFont.render("Upgrade Unlocked: Sniper Bullet", True, (255,255,255))
        screen.blit(render, (10,90))
        
    if upgrade >= 5:
        # Thriple bullet
        render = smallFont.render("Upgrade Unlocked: Thriple Bullet", True, (255,255,255))
        screen.blit(render, (10,90))

def add_upgrades_by_score(score):
    global upgrade
    if score == 3:
        upgrade = 1
    elif score == 5:
        upgrade = 2
    elif score == 7:
        upgrade = 3
    elif score == 10:
        upgrade = 4
    elif score == 12:
        upgrade = 5
    else:
        pass

# main loop
while running:

    screen.blit(pygame.image.load('grass_background.png'),(0,0))
    show_score()
    add_upgrades_by_score(score)
    enable_upgrades(upgrade)
 
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
                if not fire and not on_air:
                    milkPos[0] = player_pos[0]
                    shoot_milk(milkPos)
            
            if event.key == pygame.K_UP and upgrade >= 2 and on_air == False: 
                jump = True

        if event.type == pygame.KEYUP and not event.key == pygame.K_UP :
            go_left = False 
            go_right = False
    
    if go_left:
        if player_pos[0] > 20:
            player_pos[0] -= cow_speed
    
    if go_right:
        if player_pos[0] < 720:
            player_pos[0] += cow_speed
            
    if player_pos[1] <= 500 and player_pos[1] > 400 and jump:
        player_pos[1] -= 10
        on_air = True
    
    if player_pos[1] == 400:
        on_air = True
        jump = False
        
    if player_pos[1] >= 400 and player_pos[1] < 500 and not jump:
            player_pos[1] += 10
            jump = False
            on_air = True
    
    if player_pos[1] == 500:
        on_air = False
            
    # For each enemy in list
    for e in range(num_enemy):
        enemy(enemyImg[e], enemyPos[e])
        if enemyPos[e][0] < 20:
            horizontal_motion[e] = - horizontal_motion[e]
            
        elif enemyPos[e][0] > 750:
            horizontal_motion[e] = - horizontal_motion[e]
       
        enemyPos[e][0] += horizontal_motion[e]
        enemyPos[e][1] += vertical_motion[e]
        
        # Enemy death
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

        # Enemy wins
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
        
        # Cow kills, but it increases enemy spawn rate by 2 times !!!
        if isCollision(player_pos, enemyPos[e], 40):
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
                         
    player(player_pos[0], player_pos[1])

    # can shoot milk, only when on ground
    if fire:
        screen.blit(milkImg, milkPos)
        if milkPos[1] == player_pos[1]:
            milkPos[0] = player_pos[0]
            
        milkPos[1] -= milkSpeed
        if milkPos[1] <= 0:
            fire = False
            milkPos[1] = 500

    pygame.display.update()
    pygame.time.Clock().tick(60)
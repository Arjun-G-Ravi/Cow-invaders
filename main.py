# imports
import pygame
import random
import math
import time
import pickle

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
cow_speed = 7
jump = False
def player(x,y):
    screen.blit(playerImg, player_pos)

# Enemy
enemyImg = []
enemyPos = []
num_enemy = 3
horizontal_motion = [random.randint(1,5) for i in range(num_enemy)]
vertical_motion = [.25 for i in range(num_enemy)]

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
    monster_type = {1:['monster1.png', [random.randint(100, 700), random.randint(0, 100)], random.randint(1,5), 1+random.random()*score/250],
                    2:['monster2.png', [random.randint(100, 700), random.randint(0, 30)], random.randint(10,20)+ score/100, 1],
                    3:['monster3.png', [random.randint(100, 700), random.randint(0, 30)], random.randint(10,15)+ score/100, 2+score/200] }
    enemyImg.append(pygame.image.load(monster_type[ch][0]))
    enemyPos.append(monster_type[ch][1])
    horizontal_motion.append(monster_type[ch][2])
    vertical_motion.append(monster_type[ch][3]) 
    
# Milk
milkImg = pygame.image.load('milk1.png')
milkPos = [480,500]
fire = False
milkSpeed = 20

def shoot_milk(milkPos):
    global fire
    fire = True
    if upgrade == 3 or upgrade == 4:
        milk = pygame.mixer.Sound('gun.mp3')
        milk.play()
    else:
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

# high score

def add_high_score():
    with open('h_score.pkl', 'rb') as file:    
        data = pickle.load(file)
    return int(data)

def enable_upgrades(upgrade):
    global milkImg
    if upgrade == 0:
        render = smallFont.render("First upgrade at score 10", True, (0,0,0))
        screen.blit(render, (10,50))
        
    if upgrade == 1:
        # Cow speed up
        global cow_speed
        cow_speed = 12
        render1 = smallFont.render("Upgrades Unlocked:", True, (255,255,255))
        screen.blit(render1, (10,50))
        render = smallFont.render("    - Faster Cow", True, (255,255,255))
        screen.blit(render, (10,70))
        render = smallFont.render("Next upgrade at score 30", True, (0,0,0))
        screen.blit(render, (10,90))
        
    if upgrade == 2:
        # cow jump
        render1 = smallFont.render("Upgrades Unlocked:", True, (255,255,255))
        screen.blit(render1, (10,50))
        render = smallFont.render("    - Faster Cow", True, (255,255,255))
        screen.blit(render, (10,70))
        render = smallFont.render("    - Cow jump", True, (255,255,255))
        screen.blit(render, (10,90))
        render = smallFont.render("Next upgrade at score 50", True, (0,0,0))
        screen.blit(render, (10,110))
        
    if upgrade == 3:
        # Faster bullet
        global milkSpeed 
        milkSpeed = 40
        render1 = smallFont.render("Upgrades Unlocked:", True, (255,255,255))
        screen.blit(render1, (10,50))
        render = smallFont.render("    - Faster Cow", True, (255,255,255))
        screen.blit(render, (10,70))
        render = smallFont.render("    - Cow jump", True, (255,255,255))
        screen.blit(render, (10,90))
        render = smallFont.render("    - Faster Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,110))
        render = smallFont.render("Next upgrade at score 100", True, (0,0,0))
        screen.blit(render, (10,130))
        milkImg = pygame.image.load('milk2.png')

    if upgrade == 4:
        # Bigger bullet
        render1 = smallFont.render("Upgrades Unlocked:", True, (255,255,255))
        screen.blit(render1, (10,50))
        render = smallFont.render("    - Faster Cow", True, (255,255,255))
        screen.blit(render, (10,70))
        render = smallFont.render("    - Cow jump", True, (255,255,255))
        screen.blit(render, (10,90))
        render = smallFont.render("    - Faster Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,110))
        render = smallFont.render("    - Mega Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,130))
        render = smallFont.render("Next upgrade at score 150", True, (0,0,0))
        screen.blit(render, (10,150))
        milkSpeed = 40
        milkImg = pygame.image.load('milk3.png')
        milkImg = pygame.transform.scale(milkImg,(40,40))

    if upgrade == 5:
        # pass through bullet
        render1 = smallFont.render("Upgrades Unlocked:", True, (255,255,255))
        screen.blit(render1, (10,50))
        render = smallFont.render("    - Faster Cow", True, (255,255,255))
        screen.blit(render, (10,70))
        render = smallFont.render("    - Cow jump", True, (255,255,255))
        screen.blit(render, (10,90))
        render = smallFont.render("    - Faster Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,110))
        render = smallFont.render("    - Mega Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,130))
        render = smallFont.render("    - Ultra Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,150))
        render = smallFont.render("Next upgrade at score 300", True, (0,0,0))
        screen.blit(render, (10,170))
        milkSpeed = 20
        milkImg = pygame.image.load('milk3.png')
        milkImg = pygame.transform.scale(milkImg,(70,70))
        
    if upgrade == 6:
        # Super speed
        render1 = smallFont.render("Upgrades Unlocked:", True, (255,255,255))
        screen.blit(render1, (10,50))
        render = smallFont.render("    - Faster Cow", True, (255,255,255))
        screen.blit(render, (10,70))
        render = smallFont.render("    - Cow jump", True, (255,255,255))
        screen.blit(render, (10,90))
        render = smallFont.render("    - Faster Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,110))
        render = smallFont.render("    - Mega Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,130))
        render = smallFont.render("    - Pass through Milk Bullet", True, (255,255,255))
        screen.blit(render, (10,150))
        render = smallFont.render("    - Ultra cow", True, (255,255,255))
        screen.blit(render, (10,170))
        milkSpeed = 30
        cow_speed = 20
        
def add_upgrades_by_score(score):
    global upgrade
    
    if score == 10:
        upgrade = 1
    elif score == 30:
        upgrade = 2
    elif score == 50:
        upgrade = 3
    elif score == 100:
        upgrade = 4
    elif score == 150:
        upgrade = 5
    elif score >= 300:
        upgrade = 6
    else:
        pass

# main loop
while running:
    screen.blit(pygame.image.load('grass_background.png'),(0,0))
    show_score()
    h_score = add_high_score()
    hs_font = pygame.font.Font('freesansbold.ttf', 20)
    hs = hs_font.render(f"High Score:{h_score}", True, (255,255,255))
    screen.blit(hs, (630,30))
    add_upgrades_by_score(score)
    enable_upgrades(upgrade)
 
    for event in pygame.event.get(): 
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
        if isCollision(milkPos, enemyPos[e], distance=27 if upgrade<4 else 50):
            screen.blit(pygame.image.load('explode.png'), enemyPos[e])
            enemyPos[e] = [random.randint(100, 700), random.randint(0, 100)]
            # pygame.display.update()
            if upgrade <= 4:
                fire = False
                milkPos[1] = 500
            score += 1
            rand = random.randint(1,500)
            if rand <= 50: # 10%
                createEnemy(1)
            elif rand <= 70: # 4%
                createEnemy(2)
            elif rand <= 75: # 1%
                createEnemy(3)
            else:
                pass
            horizontal_motion[e] = random.randint(1,5) + random.random()*score/100
            vertical_motion[e] = .75
            enemyImg[e] = pygame.image.load('monster1.png')
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
                time.sleep(3)
                if score > h_score:                      
                    with open('h_score.pkl', 'wb') as file:
                        pickle.dump(str(score), file)
                        print("NEW HIGH SCORE")
                while True:
                    for event in pygame.event.get():  
                        if event.type == pygame.KEYDOWN:
                            quit(0)
        # Cow kills, but it increases enemy spawn rate by 2 times !!!
        if isCollision(player_pos, enemyPos[e], 40):
            screen.blit(pygame.image.load('explode.png'), enemyPos[e])
            enemyPos[e] = [random.randint(100, 700), random.randint(0, 100)]
            horizontal_motion[e] = random.randint(1,5) + random.random()*score/100
            vertical_motion[e] = .75
            enemyImg[e] = pygame.image.load('monster1.png')
            score += 1
            
            rand = random.randint(1,500)
            if rand <= 100: # 20%
                createEnemy(1)
            elif rand <= 140: # 8%
                createEnemy(2)
            elif rand <= 150: # 2%
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
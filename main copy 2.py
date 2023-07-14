import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT 
import random

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0, 0, 0)
PLAYER_SIZE = (20,20)



main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
#player_speed = [1, 1] - speed for random move
player_move_down = [0,1]
player_move_up = [0,-1]
player_move_right = [1,0]
player_move_left = [-1,0]

def create_enemy():
    ENEMY_SIZE = (random.randint(30, 80), random.randint(30, 80))
    ENEMY_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    enemy = pygame.Surface(ENEMY_SIZE)
    enemy.fill(ENEMY_COLOR)
    enemy_rect = pygame.Rect(WIDTH, random.randint(5, 795), *ENEMY_SIZE)
    enemy_move = [random.randint(-6, -1), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1 
pygame.time.set_timer(CREATE_ENEMY, 1500)

def create_bonuse():
    BONUSE_RADIUS = random.randint(15, 40)
    BONUSE_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    bonuse = pygame.Surface((BONUSE_RADIUS * 2, BONUSE_RADIUS * 2), pygame.SRCALPHA)
    bonuse.fill(BONUSE_COLOR)
    bonuse_rect = pygame.Rect(random.randint(5, 1195), HEIGHT, *BONUSE_RADIUS)
    bonuse_move = [random.randint(-6, -1), 0]
    return [bonuse, bonuse_rect, bonuse_move]

CREATE_BONUSE = pygame.USEREVENT + 2 
pygame.time.set_timer(CREATE_BONUSE, 1500)

enemies = []
bonuses = []
playing = True

while playing:
    FPS.tick(300)
    for event in pygame.event.get():
        if event.type == QUIT:
           playing = False 
        if event.type == CREATE_ENEMY:
           enemies.append(create_enemy())
        if event.type == CREATE_BONUSE:
           bonuses.append(create_bonuse())
            
    main_display.fill(COLOR_BLACK)
    
    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
       player_rect = player_rect.move(player_move_down)
    elif keys[K_UP] and player_rect.top > 0:
       player_rect = player_rect.move(player_move_up)
    elif keys[K_RIGHT] and player_rect.right < WIDTH:
       player_rect = player_rect.move(player_move_right)
    elif keys[K_LEFT] and player_rect.left > 0:
       player_rect = player_rect.move(player_move_left)
    
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        
    for bonuse in bonuses:
        bonuse[1] = bonuse[1].move(bonuse[2])
        main_display.blit(bonuse[0], bonuse[1])
            
    #enemy_rect = enemy_rect.move(enemy_move)
    
    ''' Random move
    # if player_rect.bottom >= HEIGHT:
    #     player_speed = random.choice(([1,-1], [-1,-1]))
    # elif player_rect.right >= WIDTH:
    #     player_speed = random.choice(([-1,1], [1,1]))
    # elif player_rect.top < 0:
    #     player_speed = random.choice(([-1,-1], [-1,1]))
    # elif player_rect.left < 0:
    #     player_speed = random.choice(([1,1], [1,-1]))
    '''      
     
    main_display.blit(player, player_rect)
    
    #main_display.blit(enemy, enemy_rect)
    
    #player_rect = player_rect.move(player_speed) - continue moving
    
    print(len(enemies))
    pygame.display.flip()
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
    
    for bonuse in bonuses:
        if bonuse[1].down() > HEIGHT:
            bonuses.pop(bonuses.index(bonuse))
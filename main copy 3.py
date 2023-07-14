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
FONT = pygame.font.SysFont("Verdana", 20)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3


player = pygame.image.load('player.png').convert_alpha() #pygame.Surface(PLAYER_SIZE)
#player.fill(COLOR_BLACK)
player_rect = player.get_rect(center=(150, 400))
player_move_down = [0,4]
player_move_up = [0,-4]
player_move_right = [4,0]
player_move_left = [-4,0]

def create_enemy():
	enemy_size = (random.randint(30, 80), random.randint(30, 80))
	#enemy_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	enemy = pygame.image.load('enemy.png').convert_alpha()#pygame.Surface(enemy_size)
	#enemy.fill(enemy_color)
	enemy_rect = pygame.Rect(WIDTH, random.randint(50, 750), *enemy_size)
	enemy_move = [random.randint(-8, -4), 0]
	return [enemy, enemy_rect, enemy_move]
CREATE_ENEMY = pygame.USEREVENT + 1 
pygame.time.set_timer(CREATE_ENEMY, 1500)

def create_bonuse():
	#bonuse_radius = random.randint(15, 40)
	#bonuse_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	bonuse = pygame.image.load('bonus.png').convert_alpha() #pygame.Surface((bonuse_radius * 2, bonuse_radius * 2), pygame.SRCALPHA)
	#pygame.draw.circle(bonuse, bonuse_color, (bonuse_radius, bonuse_radius), bonuse_radius)
	bonuse_rect = bonuse.get_rect(center=(random.randint(50, 1150), 0))
	bonuse_move = [0, random.randint(2, 8)]
	return [bonuse, bonuse_rect, bonuse_move]
CREATE_BONUSE = pygame.USEREVENT + 2 
pygame.time.set_timer(CREATE_BONUSE, 1500)

enemies = []
bonuses = []
score = 0
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
    
	bg_X1 -= bg_move
	bg_X2 -= bg_move

	if bg_X1 < -bg.get_width():
		bg_X1 = bg.get_width()

	if bg_X2 < -bg.get_width():
		bg_X2 = bg.get_width()

	main_display.blit(bg, (bg_X1, 0))	
	main_display.blit(bg, (bg_X2, 0))
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

		if player_rect.colliderect(enemy[1]):
			playing = False
        
	for bonuse in bonuses:
		bonuse[1] = bonuse[1].move(bonuse[2])
		main_display.blit(bonuse[0], bonuse[1])
		
		if player_rect.colliderect(bonuse[1]):
			score +=1
			bonuses.pop(bonuses.index(bonuse))

	main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
	main_display.blit(player, player_rect)

	pygame.display.flip()
	for enemy in enemies:
		if enemy[1].left < 0:
			enemies.pop(enemies.index(enemy))
    
	for bonuse in bonuses:
		if bonuse[1].bottom > HEIGHT:
			bonuses.pop(bonuses.index(bonuse))
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Basic Minecraft")

# Colors
GRASS = (34, 177, 76)
SKY = (135, 206, 235)
PLAYER_COLOR = (0, 0, 255)

# Grid settings
block_size = 20
cols = width // block_size
rows = height // block_size

# Simple terrain generation
terrain = [[1 if row < rows // 2 else 0 for col in range(cols)] for row in range(rows)]

# Player settings
player_x, player_y = cols // 2, rows // 2

def draw_world():
    for row in range(rows):
        for col in range(cols):
            color = GRASS if terrain[row][col] else SKY
            pygame.draw.rect(screen, color, (col * block_size, row * block_size, block_size, block_size))

def draw_player(x, y):
    pygame.draw.rect(screen, PLAYER_COLOR, (x * block_size, y * block_size, block_size, block_size))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 1
    if keys[pygame.K_RIGHT] and player_x < cols - 1:
        player_x += 1
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= 1
    if keys[pygame.K_DOWN] and player_y < rows - 1:
        player_y += 1

    screen.fill(SKY)
    draw_world()
    draw_player(player_x, player_y)
    pygame.display.flip()

pygame.quit()

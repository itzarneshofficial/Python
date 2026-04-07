import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adventure Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player settings
player_size = 50
player_x = width // 2
player_y = height - player_size
player_velocity = 5

# Item settings
item_size = 30
items = []

# Obstacle settings
obstacle_width = 50
obstacle_height = 50
obstacles = []

# Function to draw player
def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_size, player_size))

# Function to draw items
def draw_items(items):
    for item in items:
        pygame.draw.rect(screen, BLUE, (item[0], item[1], item_size, item_size))

# Function to draw obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

# Main game loop
running = True
clock = pygame.time.Clock()
score = 0

# Generate random items and obstacles
for _ in range(5):
    item_x = random.randint(0, width - item_size)
    item_y = random.randint(0, height - item_size)
    items.append([item_x, item_y])
    
    obstacle_x = random.randint(0, width - obstacle_width)
    obstacle_y = random.randint(0, height - obstacle_height)
    obstacles.append([obstacle_x, obstacle_y])

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Player movement
    if keys[pygame.K_LEFT] and player_x - player_velocity > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x + player_velocity < width - player_size:
        player_x += player_velocity
    if keys[pygame.K_UP] and player_y - player_velocity > 0:
        player_y -= player_velocity
    if keys[pygame.K_DOWN] and player_y + player_velocity < height - player_size:
        player_y += player_velocity

    # Collect items
    for item in items[:]:
        if player_x < item[0] + item_size and player_x + player_size > item[0] and \
           player_y < item[1] + item_size and player_y + player_size > item[1]:
            items.remove(item)
            score += 1

    # Collision detection with obstacles
    for obstacle in obstacles:
        if player_x < obstacle[0] + obstacle_width and player_x + player_size > obstacle[0] and \
           player_y < obstacle[1] + obstacle_height and player_y + player_size > obstacle[1]:
            running = False

    # Draw player, items, and obstacles
    draw_player(player_x, player_y)
    draw_items(items)
    draw_obstacles(obstacles)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("Your score:", score)

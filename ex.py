import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
player_size = 50
player_x = width // 2
player_y = height - 2 * player_size
player_velocity = 10

# Obstacle settings
obstacle_width = 50
obstacle_height = 50
obstacle_velocity = 7
obstacles = []

# Function to draw player
def draw_player(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, player_size, player_size))

# Function to draw obstacles
def draw_obstacle(x, y):
    pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))

# Main game loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and player_x - player_velocity > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x + player_velocity < width - player_size:
        player_x += player_velocity

    if random.randint(1, 20) == 1:
        obstacle_x = random.randint(0, width - obstacle_width)
        obstacles.append([obstacle_x, -obstacle_height])

    for obstacle in obstacles:
        obstacle[1] += obstacle_velocity
        if obstacle[1] > height:
            obstacles.remove(obstacle)
            score += 1

    draw_player(player_x, player_y)

    for obstacle in obstacles:
        draw_obstacle(obstacle[0], obstacle[1])
        if player_x < obstacle[0] + obstacle_width and player_x + player_size > obstacle[0] and player_y < obstacle[1] + obstacle_height and player_y + player_size > obstacle[1]:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

print("Your score:", score)

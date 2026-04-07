import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Driving Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
car_width = 50
car_height = 100
car_x = width // 2 - car_width // 2
car_y = height - car_height - 10
car_velocity = 7

# Obstacle settings
obstacle_width = 50
obstacle_height = 100
obstacle_velocity = 7
obstacles = []
obstacle_spawn_rate = 30  # Lower value means more obstacles

# Function to draw car
def draw_car(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, car_width, car_height))

# Function to draw obstacles
def draw_obstacle(x, y):
    pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))

# Main game loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Car movement
    if keys[pygame.K_LEFT] and car_x - car_velocity > 0:
        car_x -= car_velocity
    if keys[pygame.K_RIGHT] and car_x + car_velocity < width - car_width:
        car_x += car_velocity

    # Spawn obstacles
    if random.randint(1, obstacle_spawn_rate) == 1:
        obstacle_x = random.randint(0, width - obstacle_width)
        obstacles.append([obstacle_x, -obstacle_height])

    # Move obstacles
    for obstacle in obstacles:
        obstacle[1] += obstacle_velocity
        if obstacle[1] > height:
            obstacles.remove(obstacle)
            score += 1

    # Collision detection
    for obstacle in obstacles:
        if car_x < obstacle[0] + obstacle_width and car_x + car_width > obstacle[0] and \
           car_y < obstacle[1] + obstacle_height and car_y + car_height > obstacle[1]:
            running = False

    # Draw car and obstacles
    draw_car(car_x, car_y)
    for obstacle in obstacles:
        draw_obstacle(obstacle[0], obstacle[1])

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("Your score:", score)

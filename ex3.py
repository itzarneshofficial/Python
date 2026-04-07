import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width = 50
player_height = 30
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_velocity = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_velocity =4
bullets = []

# Enemy settings
enemy_width = 50
      
enemy_height = 30
enemy_velocity = 2
enemies = []
enemy_spawn_rate = 30  # Lower value means more enemies

# Function to draw player
def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_width, player_height))

# Function to draw bullets
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))

# Function to draw enemies
def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

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

    # Player movement
    if keys[pygame.K_LEFT] and player_x - player_velocity > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x + player_velocity < width - player_width:
        player_x += player_velocity

    # Shooting bullets
    if keys[pygame.K_SPACE]:
        bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_velocity
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Spawn enemies
    if random.randint(1, enemy_spawn_rate) == 1:
        enemy_x = random.randint(0, width - enemy_width)
        enemies.append([enemy_x, -enemy_height])

    # Move enemies
    for enemy in enemies:
        enemy[1] += enemy_velocity
        if enemy[1] > height:
            enemies.remove(enemy)

    # Collision detection
    for enemy in enemies:
        for bullet in bullets:
            if enemy[0] < bullet[0] < enemy[0] + enemy_width and \
               enemy[1] < bullet[1] < enemy[1] + enemy_height:
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1

    # Draw player, bullets, and enemies
    draw_player(player_x, player_y)
    draw_bullets(bullets)
    draw_enemies(enemies)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("Your score:", score)

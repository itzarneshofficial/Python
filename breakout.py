import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# Paddle settings
paddle_width = 100
paddle_height = 10
paddle_speed = 10

# Ball settings
ball_size = 10
ball_speed_x = 5
ball_speed_y = -5

# Brick settings
brick_rows = 5
brick_cols = 10
brick_width = 70
brick_height = 20
brick_margin = 5

# Paddle position
paddle_x = width // 2 - paddle_width // 2
paddle_y = height - 30

# Ball position
ball_x = width // 2 - ball_size // 2
ball_y = height // 2 - ball_size // 2

# Create bricks
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_margin) + brick_margin
        brick_y = row * (brick_height + brick_margin) + brick_margin
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
        paddle_x += paddle_speed

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_y <= 0:
        ball_speed_y *= -1
    if ball_x <= 0 or ball_x >= width - ball_size:
        ball_speed_x *= -1
    if ball_y >= height:
        ball_x = width // 2 - ball_size // 2
        ball_y = height // 2 - ball_size // 2
        ball_speed_x *= random.choice([-1, 1])
        ball_speed_y *= random.choice([-1, 1])

    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)

    if paddle_rect.colliderect(ball_rect):
        ball_speed_y *= -1

    for brick in bricks[:]:
        if brick.colliderect(ball_rect):
            bricks.remove(brick)
            ball_speed_y *= -1
            break

    screen.fill(black)
    pygame.draw.rect(screen, white, paddle_rect)
    pygame.draw.ellipse(screen, blue, ball_rect)
    for brick in bricks:
        pygame.draw.rect(screen, red, brick)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

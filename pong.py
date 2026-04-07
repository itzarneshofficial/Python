import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Paddle settings
paddle_width = 10
paddle_height = 100
paddle_speed = 10

# Ball settings
ball_size = 10
ball_speed_x = 5
ball_speed_y = 5

# Paddle positions
left_paddle_y = height // 2 - paddle_height // 2
right_paddle_y = height // 2 - paddle_height // 2

# Ball position
ball_x = width // 2 - ball_size // 2
ball_y = height // 2 - ball_size // 2

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < height - paddle_height:
        left_paddle_y += paddle_speed
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle_y < height - paddle_height:
        right_paddle_y += paddle_speed

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_y <= 0 or ball_y >= height - ball_size:
        ball_speed_y *= -1
    if ball_x <= paddle_width and left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
        ball_speed_x *= -1
    if ball_x >= width - paddle_width - ball_size and right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
        ball_speed_x *= -1
    if ball_x <= 0 or ball_x >= width - ball_size:
        ball_x = width // 2 - ball_size // 2
        ball_y = height // 2 - ball_size // 2
        ball_speed_x *= random.choice([-1, 1])
        ball_speed_y *= random.choice([-1, 1])

    screen.fill(black)
    pygame.draw.rect(screen, white, (0, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (width - paddle_width, right_paddle_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, white, (ball_x, ball_y, ball_size, ball_size))
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

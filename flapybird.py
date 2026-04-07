import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)

# Bird settings
bird_width = 40
bird_height = 40
bird_x = width // 4
bird_y = height // 2
bird_speed = 0
gravity = 0.5
jump = -10

# Pipe settings
pipe_width = 70
pipe_height = random.randint(150, 450)
pipe_x = width
pipe_gap = 200
pipe_speed = 3

# Game variables
score = 0
game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_speed = jump

    bird_speed += gravity
    bird_y += bird_speed

    pipe_x -= pipe_speed
    if pipe_x < -pipe_width:
        pipe_x = width
        pipe_height = random.randint(150, 450)
        score += 1

    screen.fill(blue)
    pygame.draw.rect(screen, green, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(screen, green, (pipe_x, pipe_height + pipe_gap, pipe_width, height - pipe_height - pipe_gap))
    pygame.draw.rect(screen, white, (bird_x, bird_y, bird_width, bird_height))

    if bird_y > height or bird_y < 0 or (pipe_x < bird_x + bird_width < pipe_x + pipe_width and (bird_y < pipe_height or bird_y + bird_height > pipe_height + pipe_gap)):
        game_over = True

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()

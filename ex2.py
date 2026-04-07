import pygame

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
paddle_width = 10
paddle_height = 100
paddle_velocity = 7

# Player positions
player1_x, player1_y = 50, height // 2 - paddle_height // 2
player2_x, player2_y = width - 50 - paddle_width, height // 2 - paddle_height // 2

# Ball settings
ball_radius = 10
ball_x, ball_y = width // 2, height // 2
ball_velocity_x, ball_velocity_y = 5, 5

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Player 1 controls (W and S keys)
    if keys[pygame.K_w] and player1_y - paddle_velocity > 0:
        player1_y -= paddle_velocity
    if keys[pygame.K_s] and player1_y + paddle_velocity < height - paddle_height:
        player1_y += paddle_velocity

    # Player 2 controls (UP and DOWN keys)
    if keys[pygame.K_UP] and player2_y - paddle_velocity > 0:
        player2_y -= paddle_velocity
    if keys[pygame.K_DOWN] and player2_y + paddle_velocity < height - paddle_height:
        player2_y += paddle_velocity

    # Move the ball
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Ball collision with top and bottom walls
    if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
        ball_velocity_y *= -1

    # Ball collision with paddles
    if (ball_x - ball_radius < player1_x + paddle_width and player1_y < ball_y < player1_y + paddle_height) or \
       (ball_x + ball_radius > player2_x and player2_y < ball_y < player2_y + paddle_height):
        ball_velocity_x *= -1

    # Ball reset after missing paddle
    if ball_x < 0 or ball_x > width:
        ball_x, ball_y = width // 2, height // 2
        ball_velocity_x *= -1

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (player1_x, player1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (player2_x, player2_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple House")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# House settings
house_x = 300
house_y = 300
house_width = 200
house_height = 200

# Function to draw the house
def draw_house():
    # Draw the base of the house
    pygame.draw.rect(screen, RED, (house_x, house_y, house_width, house_height))

    # Draw the roof
    pygame.draw.polygon(screen, BROWN, [(house_x, house_y), (house_x + house_width, house_y), (house_x + house_width / 2, house_y - house_height / 2)])

    # Draw the door
    pygame.draw.rect(screen, BLUE, (house_x + house_width / 2 - 25, house_y + house_height - 50, 50, 50))

    # Draw windows
    pygame.draw.rect(screen, WHITE, (house_x + 20, house_y + 20, 40, 40))
    pygame.draw.rect(screen, WHITE, (house_x + house_width - 60, house_y + 20, 40, 40))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GREEN)  # Background color

    draw_house()
    
    pygame.display.flip()

pygame.quit()

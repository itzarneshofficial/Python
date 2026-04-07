import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 300, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
colors = [
    (0, 255, 255),
    (255, 165, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 0),
    (128, 0, 128)
]

# Tetrimino shapes
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Game variables
grid = [[0 for _ in range(10)] for _ in range(20)]
current_shape = random.choice(shapes)
current_color = random.choice(colors)
current_x, current_y = 3, 0
clock = pygame.time.Clock()

def draw_grid():
    for y in range(20):
        for x in range(10):
            if grid[y][x] != 0:
                pygame.draw.rect(screen, grid[y][x], (x * 30, y * 30, 30, 30))

def draw_shape():
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_color, ((current_x + x) * 30, (current_y + y) * 30, 30, 30))

def check_collision():
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                if current_y + y >= 20 or current_x + x < 0 or current_x + x >= 10 or grid[current_y + y][current_x + x]:
                    return True
    return False

def merge_shape():
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                grid[current_y + y][current_x + x] = current_color

def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < 20:
        grid.insert(0, [0 for _ in range(10)])

def new_shape():
    global current_shape, current_color, current_x, current_y
    current_shape = random.choice(shapes)
    current_color = random.choice(colors)
    current_x, current_y = 3, 0

# Game loop
running = True
while running:
    screen.fill(black)
    draw_grid()
    draw_shape()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_x -= 1
                if check_collision():
                    current_x += 1
            elif event.key == pygame.K_RIGHT:
                current_x += 1
                if check_collision():
                    current_x -= 1
            elif event.key == pygame.K_DOWN:
                current_y += 1
                if check_collision():
                    current_y -= 1
            elif event.key == pygame.K_UP:
                current_shape = [list(row) for row in zip(*current_shape[::-1])]
                if check_collision():
                    current_shape = [list(row) for row in zip(*current_shape[::-1])][::-1]

    current_y += 1
    if check_collision():
        current_y -= 1
        merge_shape()
        clear_lines()
        new_shape()
        if check_collision():
            running = False

    clock.tick(10)

pygame.quit()

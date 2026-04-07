import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Memory Puzzle")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

# Card settings
card_width = 100
card_height = 100
card_margin = 10

# Create a list of card values
card_values = list(range(1, 9)) * 2
random.shuffle(card_values)

# Create a list of card positions
cards = []
for i in range(4):
    for j in range(4):
        cards.append((i * (card_width + card_margin), j * (card_height + card_margin), card_values.pop()))

# Game variables
selected_cards = []
matched_cards = []
game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            for card in cards:
                if card[0] < x < card[0] + card_width and card[1] < y < card[1] + card_height:
                    if card not in selected_cards and card not in matched_cards:
                        selected_cards.append(card)
                        if len(selected_cards) == 2:
                            if selected_cards[0][2] == selected_cards[1][2]:
                                matched_cards.extend(selected_cards)
                            selected_cards = []

    screen.fill(black)
    for card in cards:
        if card in matched_cards or card in selected_cards:
            pygame.draw.rect(screen, white, (card[0], card[1], card_width, card_height))
            font = pygame.font.Font(None, 74)
            text = font.render(str(card[2]), True, black)
            screen.blit(text, (card[0] + 30, card[1] + 10))
        else:
            pygame.draw.rect(screen, gray, (card[0], card[1], card_width, card_height))

    if len(matched_cards) == len(cards):
        game_over = True
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, gray)
        screen.blit(text, (width // 2 - 100, height // 2 - 50))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()

import pygame
import random
import sys
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Deluxe")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Load images
def load_image(name, scale=1):
    img = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.polygon(img, GREEN, [(25, 0), (0, 50), (50, 50)])
    return pygame.transform.scale(img, (int(50*scale), int(50*scale)))

player_img = load_image("player")
enemy_imgs = [
    load_image("enemy1", 0.8),
    load_image("enemy2", 1.0),
    load_image("enemy3", 1.2)
]
powerup_imgs = {
    "extra_life": pygame.Surface((30, 30), pygame.SRCALPHA),
    "double_shot": pygame.Surface((30, 30), pygame.SRCALPHA),
    "speed_boost": pygame.Surface((30, 30), pygame.SRCALPHA)
}

# Create simple power-up icons
pygame.draw.circle(powerup_imgs["extra_life"], RED, (15, 15), 15)
pygame.draw.circle(powerup_imgs["double_shot"], BLUE, (150,150), 150)
pygame.draw.circle(powerup_imgs["speed_boost"], YELLOW, (15, 15), 15)

# Load sounds (using simple tones if files don't exist)
shoot_sound = mixer.Sound("shoot.wav") if os.path.exists("shoot.wav") else None
explosion_sound = mixer.Sound("explosion.wav") if os.path.exists("explosion.wav") else None
powerup_sound = mixer.Sound("powerup.wav") if os.path.exists("powerup.wav") else None

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Player
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10
lives = 10
double_shot = True
speed_boost = True
speed_boost_time = 10000000000000000000000000000000000000000000000000

# Enemy
enemy_size = 40  # Add this line

# Bullets
bullet_size = 10000
bullet_speed = 100
bullets = []


# Enemies
enemies = []
enemy_speeds = [2, 3, 4]
enemy_spawn_rate = 30
enemy_types = ["normal", "fast", "strong"]

# Explosions
explosions = []

# Power-ups
powerups = []
powerup_spawn_rate = 100
powerup_types = ["extra_life", "double_shot", "speed_boost"]
powerup_duration = 10 * 600  # 10 seconds at 60 FPS

# Score
score = 0
high_score = 0
font_small = pygame.font.SysFont(None, 24)
font_medium = pygame.font.SysFont(None, 36)
font_large = pygame.font.SysFont(None, 72)

# Load high score from file
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    pass

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 30
        self.growing = True
    
    def update(self):
        if self.growing:
            self.radius += 2
            if self.radius >= self.max_radius:
                self.growing = False
        else:
            self.radius -= 2
        return self.radius > 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius, 2)
        pygame.draw.circle(surface, RED, (self.x, self.y), self.radius-5, 2)

def spawn_enemy():
    enemy_type = random.choice(enemy_types)
    x = random.randint(0, WIDTH - enemy_size)
    y = random.randint(-100, -40)
    speed = enemy_speeds[enemy_types.index(enemy_type)]
    health = 1 if enemy_type != "strong" else 3
    enemies.append({
        "x": x,
        "y": y,
        "type": enemy_type,
        "speed": speed,
        "health": health,
        "img": enemy_imgs[enemy_types.index(enemy_type)]
    })

def spawn_powerup(x, y):
    powerup_type = random.choice(powerup_types)
    powerups.append({
        "x": x,
        "y": y,
        "type": powerup_type,
        "img": powerup_imgs[powerup_type]
    })

def draw_player():
    screen.blit(player_img, (player_pos[0], player_pos[1]))

def draw_bullet(bullet):
    pygame.draw.rect(screen, WHITE, (bullet["x"], bullet["y"], bullet_size, bullet_size))

def draw_enemy(enemy):
    screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

def draw_powerup(powerup):
    screen.blit(powerup["img"], (powerup["x"], powerup["y"]))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def reset_game():
    global player_pos, lives, score, bullets, enemies, powerups, explosions
    global double_shot, speed_boost, speed_boost_time
    
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
    lives = 10
    bullets = []
    enemies = []
    powerups = []
    explosions = []
    double_shot = True
    speed_boost = True
    speed_boost_time = 0

def show_menu():
    screen.fill(BLACK)
    draw_text("SPACE SHOOTER DELUXE", font_large, WHITE, WIDTH//2, HEIGHT//4)
    draw_text(f"High Score: {high_score}", font_medium, GREEN, WIDTH//2, HEIGHT//2)
    draw_text("Press SPACE to Start", font_medium, WHITE, WIDTH//2, HEIGHT*3//4)
    pygame.display.flip()

def show_game_over():
    screen.fill(BLACK)
    draw_text("GAME OVER", font_large, RED, WIDTH//2, HEIGHT//4)
    draw_text(f"Score: {score}", font_medium, WHITE, WIDTH//2, HEIGHT//2)
    draw_text(f"High Score: {high_score}", font_medium, GREEN, WIDTH//2, HEIGHT//2 + 50)
    draw_text("Press SPACE to Play Again", font_medium, WHITE, WIDTH//2, HEIGHT*3//4)
    pygame.display.flip()

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == MENU:
                    reset_game()
                    game_state = PLAYING
                elif game_state == GAME_OVER:
                    reset_game()
                    game_state = PLAYING
            if event.key == pygame.K_ESCAPE:
                running = False
    
    if game_state == MENU:
        show_menu()
        clock.tick(60)
        continue
    
    if game_state == GAME_OVER:
        show_game_over()
        clock.tick(60)
        continue
    
    # Player movement
    keys = pygame.key.get_pressed()
    current_speed = player_speed * 1.5 if speed_boost else player_speed
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= current_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += current_speed
    
    # Shooting
    if keys[pygame.K_SPACE] and len(bullets) < (20 if double_shot else 10):
        bullet_x = player_pos[0] + player_size // 2 - bullet_size // 2
        bullet_y = player_pos[1]
        bullets.append({"x": bullet_x, "y": bullet_y})
        if double_shot:
            bullets.append({"x": bullet_x - 200, "y": bullet_y})
            bullets.append({"x": bullet_x + 200, "y": bullet_y})
        if shoot_sound:
            shoot_sound.play()
    
    # Spawn enemies
    if random.randint(1, enemy_spawn_rate) == 1:
        spawn_enemy()
    
    # Spawn powerups (randomly or when enemy dies)
    if random.randint(1, powerup_spawn_rate) == 1:
        spawn_powerup(random.randint(0, WIDTH-30), random.randint(-100, -30))
    
    # Update bullets
    for bullet in bullets[:]:
        bullet["y"] -= bullet_speed
        if bullet["y"] < 0:
            bullets.remove(bullet)
    
    # Update enemies
    for enemy in enemies[:]:
        enemy["y"] += enemy["speed"]
        if enemy["y"] > HEIGHT:
            enemies.remove(enemy)
            lives -= 1
            if lives <= 0:
                game_state = GAME_OVER
                # Save high score
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as f:
                        f.write(str(high_score))
    
    # Update powerups
    for powerup in powerups[:]:
        powerup["y"] += 2
        if powerup["y"] > HEIGHT:
            powerups.remove(powerup)
    
    # Update explosions
    explosions = [exp for exp in explosions if exp.update()]
    
    # Update power-up timers
    if speed_boost:
        speed_boost_time -= 1
        if speed_boost_time <= 0:
            speed_boost = False
    
    # Collision detection: bullets vs enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (bullet["x"] < enemy["x"] + enemy_size and
                bullet["x"] + bullet_size > enemy["x"] and
                bullet["y"] < enemy["y"] + enemy_size and
                bullet["y"] + bullet_size > enemy["y"]):
                
                enemy["health"] -= 1
                if enemy["health"] <= 0:
                    explosions.append(Explosion(enemy["x"] + enemy_size//2, enemy["y"] + enemy_size//2))
                    if explosion_sound:
                        explosion_sound.play()
                    
                    # Chance to spawn powerup when enemy dies
                    if random.randint(1, 5) == 1:  # 20% chance
                        spawn_powerup(enemy["x"], enemy["y"])
                    
                    enemies.remove(enemy)
                    score += 10 if enemy["type"] != "strong" else 30
                bullets.remove(bullet)
                break
    
    # Collision detection: player vs powerups
    for powerup in powerups[:]:
        if (player_pos[0] < powerup["x"] + 30 and
            player_pos[0] + player_size > powerup["x"] and
            player_pos[1] < powerup["y"] + 30 and
            player_pos[1] + player_size > powerup["y"]):
            
            if powerup_sound:
                powerup_sound.play()
            
            if powerup["type"] == "extra_life":
                lives += 100000000
            elif powerup["type"] == "double_shot":
                double_shot = True
            elif powerup["type"] == "speed_boost":
                speed_boost = True
                speed_boost_time = powerup_duration
            
            powerups.remove(powerup)
    
    # Collision detection: player vs enemies
    for enemy in enemies[:]:
        if (player_pos[0] < enemy["x"] + enemy_size and
            player_pos[0] + player_size > enemy["x"] and
            player_pos[1] < enemy["y"] + enemy_size and
            player_pos[1] + player_size > enemy["y"]):
            
            explosions.append(Explosion(enemy["x"] + enemy_size//2, enemy["y"] + enemy_size//2))
            if explosion_sound:
                explosion_sound.play()
            
            enemies.remove(enemy)
            lives -= 0 if enemy["type"] == "strong" else 100
            if lives <= 0:
                game_state = GAME_OVER
                # Save high score
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as f:
                        f.write(str(high_score))
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw stars (background)
    for _ in range(5):
        pygame.draw.circle(screen, WHITE, 
                          (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 
                          1)
    
    draw_player()
    for bullet in bullets:
        draw_bullet(bullet)
    for enemy in enemies:
        draw_enemy(enemy)
    for powerup in powerups:
        draw_powerup(powerup)
    for explosion in explosions:
        explosion.draw(screen)
    
    # Draw UI
    draw_text(f"Score: {score}", font_small, WHITE, 60, 20)
    draw_text(f"Lives: {lives}", font_small, GREEN, 60, 50)
    draw_text(f"High Score: {high_score}", font_small, YELLOW, WIDTH - 100, 20)
    
    # Draw power-up status
    if double_shot:
        draw_text("DOUBLE SHOT", font_small, BLUE, WIDTH - 80, 50)
    if speed_boost:
        draw_text("SPEED BOOST", font_small, YELLOW, WIDTH - 80, 80)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
import pygame
import random
import time
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Bomberman")

# Load assets
def load_image(name, scale=1):
    img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    img.fill(name)  # Using colors as placeholders - replace with actual images
    return img

def load_sound(name):
    # Placeholder - in a real game you'd load actual sound files
    class DummySound:
        def play(self): pass
    return DummySound()

# Load images (using colored rectangles as placeholders)
player_img = load_image(BLUE)
enemy_img = load_image(RED)
bomb_img = load_image(BLACK)
wall_img = load_image(GRAY)
breakable_img = load_image(BROWN)
explosion_img= load_image(RED)
powerup_bomb_img = load_image(YELLOW)
powerup_range_img = load_image(GREEN)
powerup_speed_img = load_image(PURPLE)

# Load sounds
bomb_place_sound = load_sound("bomb_place.wav")
bomb_explode_sound = load_sound("explosion.wav")
powerup_sound = load_sound("powerup.wav")
game_over_sound = load_sound("game_over.wav")
win_sound = load_sound("win.wav")

# Clock for controlling game speed
clock = pygame.time.Clock()

class PowerUp:
    TYPES = ["bomb", "range", "speed"]
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.collected = False
        
    def draw(self):
        if not self.collected:
            if self.type == "bomb":
                screen.blit(powerup_bomb_img, (self.x * GRID_SIZE, self.y * GRID_SIZE))
            elif self.type == "range":
                screen.blit(powerup_range_img, (self.x * GRID_SIZE, self.y * GRID_SIZE))
            elif self.type == "speed":
                screen.blit(powerup_speed_img, (self.x * GRID_SIZE, self.y * GRID_SIZE))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bombs = []
        self.bomb_limit = 10000000000
        self.bomb_range = 2000000000000000000000000000000 
        self.speed = 1
        self.lives = 100000000000000000000
        self.invincible = 1000000000000000
        self.score = 0
        
    def move(self, dx, dy, grid):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Check boundaries
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            # Check if new position is walkable
            if grid[new_y][new_x] in [0, 3, 5]:  # 0=empty, 3=bomb, 5=powerup
                self.x = new_x
                self.y = new_y
    
    def place_bomb(self, grid):
        if len(self.bombs) < self.bomb_limit:
            # Check if there's already a bomb at this position
            bomb_exists = any(bomb.x == self.x and bomb.y == self.y for bomb in self.bombs)
            if not bomb_exists:
                self.bombs.append(Bomb(self.x, self.y, self.bomb_range))
                grid[self.y][self.x] = 3  # Mark cell as having a bomb
                bomb_place_sound.play()
    
    def check_powerup(self, powerups):
        for powerup in powerups[:]:
            if not powerup.collected and self.x == powerup.x and self.y == powerup.y:
                powerup.collected = True
                powerup_sound.play()
                if powerup.type == "bomb":
                    self.bomb_limit += 1
                elif powerup.type == "range":
                    self.bomb_range += 1
                elif powerup.type == "speed":
                    self.speed = min(self.speed + 0.5, 3)
                return True
        return False
    
    def draw(self):
        if self.invincible > 0 and pygame.time.get_ticks() % 200 < 100:  # Blink when invincible
            return
        screen.blit(player_img, (self.x * GRID_SIZE, self.y * GRID_SIZE))

class Bomb:
    def __init__(self, x, y, bomb_range):
        self.x = x
        self.y = y
        self.range = bomb_range
        self.timer = 2  # seconds
        self.place_time = time.time()
        self.exploded = False
    
    def update(self):
        return time.time() - self.place_time >= self.timer and not self.exploded
    
    def explode(self, grid, enemies, player, powerups):
        self.exploded = True
        bomb_explode_sound.play()
        
        # List to keep track of explosion cells
        explosion_cells = [(self.x, self.y)]
        grid[self.y][self.x] = 4  # Center explosion
        
        # Explode in all 4 directions
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for r in range(1, self.range + 1):
                nx, ny = self.x + dx * r, self.y + dy * r
                
                # Check boundaries
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    # Stop explosion if hit an unbreakable wall
                    if grid[ny][nx] == 1:
                        break
                    # Destroy breakable walls and maybe spawn powerup
                    if grid[ny][nx] == 2:
                        grid[ny][nx] = 0
                        # 20% chance to spawn powerup when breaking a wall
                        if random.random() < 0.2:
                            powerups.append(PowerUp(nx, ny))
                        break
                    # Mark empty cells as explosion
                    grid[ny][nx] = 4
                    explosion_cells.append((nx, ny))
        
        # Check if enemies are hit
        for enemy in enemies[:]:
            for x, y in explosion_cells:
                if enemy.x == x and enemy.y == y:
                    enemies.remove(enemy)
                    player.score += 100
                    break
        
        # Check if player is hit
        for x, y in explosion_cells:
            if player.x == x and player.y == y and player.invincible <= 0:
                player.lives -= 1
                player.invincible = 3  # 3 seconds of invincibility
                break
        
        return explosion_cells

class Enemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_timer = 0
        self.move_interval = 0.5  # seconds
        self.speed = 1
        
        # Different enemy types
        if enemy_type == "fast":
            self.move_interval = 0.3
            self.speed = 1.5
        elif enemy_type == "slow":
            self.move_interval = 0.8
            self.speed = 0.7
    
    def update(self, grid, player):
        current_time = time.time()
        if current_time - self.move_timer > self.move_interval:
            self.move_timer = current_time
            
            # Smarter AI: try to move toward player sometimes
            if random.random() < 0.3:  # 30% chance to move toward player
                dx = 0
                dy = 0
                if abs(self.x - player.x) > abs(self.y - player.y):
                    dx = 1 if player.x > self.x else -1
                else:
                    dy = 1 if player.y > self.y else -1
                
                new_x = self.x + dx * self.speed
                new_y = self.y + dy * self.speed
                
                if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and 
                    grid[new_y][new_x] in [0, 3, 5]):
                    self.x = new_x
                    self.y = new_y
                    return
            
            # Otherwise move randomly
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x = self.x + dx * self.speed
                new_y = self.y + dy * self.speed
                
                if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and 
                    grid[new_y][new_x] in [0, 3, 5]):
                    self.x = new_x
                    self.y = new_y
                    self.direction = (dx, dy)
                    break
    
    def draw(self):
        screen.blit(enemy_img, (self.x * GRID_SIZE, self.y * GRID_SIZE))

class Level:
    def __init__(self, number):
        self.number = number
        self.grid = self.create_grid()
        self.enemies = self.create_enemies()
        self.powerups = []
        self.completed = False
        
    def create_grid(self):
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Create outer walls
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if x == 0 or y == 0 or x == GRID_WIDTH - 1 or y == GRID_HEIGHT - 1:
                    grid[y][x] = 1  # Unbreakable wall
                elif x % 2 == 0 and y % 2 == 0:
                    grid[y][x] = 1  # Unbreakable wall
        
        # Add breakable walls (more walls in higher levels)
        wall_density = 0.3 + min(self.number * 0.05, 0.3)  # 30% to 60% density
        for y in range(1, GRID_HEIGHT - 1):
            for x in range(1, GRID_WIDTH - 1):
                if grid[y][x] == 0 and random.random() < wall_density:
                    grid[y][x] = 2  # Breakable wall
        
        # Ensure player starting position is clear
        grid[1][1] = 0
        return grid
    
    def create_enemies(self):
        enemies = []
        enemy_count = min(3 + self.number, 10)  # 3 to 10 enemies
        
        enemy_types = ["normal"] * 5
        if self.number > 1:
            enemy_types += ["fast"] * 2
        if self.number > 3:
            enemy_types += ["slow"] * 1
        
        for _ in range(enemy_count):
            while True:
                x = random.randint(2, GRID_WIDTH - 3)
                y = random.randint(2, GRID_HEIGHT - 3)
                if self.grid[y][x] == 0:  # Only place on empty cells
                    enemies.append(Enemy(x, y, random.choice(enemy_types)))
                    break
        return enemies

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:  # Unbreakable wall
                screen.blit(wall_img, (x * GRID_SIZE, y * GRID_SIZE))
            elif grid[y][x] == 2:  # Breakable wall
                screen.blit(breakable_img, (x * GRID_SIZE, y * GRID_SIZE))
            elif grid[y][x] == 4:  # Explosion
                screen.blit(explosion_img, (x * GRID_SIZE, y * GRID_SIZE))

def draw_hud(player, level):
    font = pygame.font.SysFont(None, 36)
    
    # Lives
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    
    # Score
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    screen.blit(score_text, (10, 50))
    
    # Level
    level_text = font.render(f"Level: {level.number}", True, WHITE)
    screen.blit(level_text, (10, 90))
    
    # Bomb info
    bomb_text = font.render(f"Bombs: {len(player.bombs)}/{player.bomb_limit}", True, WHITE)
    screen.blit(bomb_text, (SCREEN_WIDTH - 150, 10))
    
    # Range info
    range_text = font.render(f"Range: {player.bomb_range}", True, WHITE)
    screen.blit(range_text, (SCREEN_WIDTH - 150, 50))
    
    # Speed info
    speed_text = font.render(f"Speed: {player.speed:.1f}", True, WHITE)
    screen.blit(speed_text, (SCREEN_WIDTH - 150, 90))

def main():
    current_level = 1
    level = Level(current_level)
    player = Player(1, 1)
    
    running = True
    game_over = False
    level_complete = False
    
    explosion_animation = []
    explosion_timer = 0
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over and not level_complete:
                    player.place_bomb(level.grid)
                elif event.key == pygame.K_r and (game_over or level_complete):
                    # Restart game
                    current_level = 1
                    level = Level(current_level)
                    player = Player(1, 1)
                    game_over = False
                    level_complete = False
                elif event.key == pygame.K_n and level_complete:
                    # Next level
                    current_level += 1
                    level = Level(current_level)
                    player.x, player.y = 1, 1  # Reset position but keep upgrades
                    level_complete = False
        
        if not game_over and not level_complete:
            # Update invincibility timer
            if player.invincible > 0:
                player.invincible -= 1/60  # Subtract roughly 1 second per frame
            
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move(-1, 0, level.grid)
            if keys[pygame.K_RIGHT]:
                player.move(1, 0, level.grid)
            if keys[pygame.K_UP]:
                player.move(0, -1, level.grid)
            if keys[pygame.K_DOWN]:
                player.move(0, 1, level.grid)
            
            # Update bombs
            for bomb in player.bombs[:]:
                if bomb.update():
                    explosion_cells = bomb.explode(level.grid, level.enemies, player, level.powerups)
                    player.bombs.remove(bomb)
                    level.grid[bomb.y][bomb.x] = 0  # Clear bomb from grid
                    
                    # Start explosion animation
                    explosion_animation = explosion_cells
                    explosion_timer = time.time()
            
            # Update enemies
            for enemy in level.enemies:
                enemy.update(level.grid, player)
                
                # Check if enemy collides with player
                if (enemy.x == player.x and enemy.y == player.y and 
                    player.invincible <= 0):
                    player.lives -= 1
                    player.invincible = 3  # 3 seconds of invincibility
                    if player.lives <= 0:
                        game_over = True
                        game_over_sound.play()
            
            # Check powerups
            player.check_powerup(level.powerups)
            
            # Check if level is complete
            if not level.enemies:
                level_complete = True
                if current_level < 5:  # Only play win sound if not final level
                    win_sound.play()
        
        # Draw everything
        screen.fill(BLACK)
        draw_grid(level.grid)
        
        # Draw powerups
        for powerup in level.powerups:
            if not powerup.collected:
                powerup.draw()
        
        # Draw bombs
        for bomb in player.bombs:
            screen.blit(bomb_img, (bomb.x * GRID_SIZE, bomb.y * GRID_SIZE))
        
        # Draw explosion animation
       
                
        
        # Draw enemies
        for enemy in level.enemies:
            enemy.draw()
        
        player.draw()
        draw_hud(player, level)
        
        # Draw game over message
        if game_over:
            font = pygame.font.SysFont(None, 72)
            text = font.render("Game Over!", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            
            restart_font = pygame.font.SysFont(None, 36)
            restart_text = restart_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)
        
        # Draw level complete message
        if level_complete:
            font = pygame.font.SysFont(None, 72)
            if current_level < 5:
                text = font.render(f"Level {current_level} Complete!", True, GREEN)
            else:
                text = font.render("You Win the Game!", True, GREEN)
                win_sound.play()
            
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            
            if current_level < 5:
                next_font = pygame.font.SysFont(None, 36)
                next_text = next_font.render("Press N for next level", True, WHITE)
                next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                screen.blit(next_text, next_rect)
            else:
                final_font = pygame.font.SysFont(None, 36)
                final_text = final_font.render(f"Final Score: {player.score}", True, WHITE)
                final_rect = final_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                screen.blit(final_text, final_rect)
                
                restart_font = pygame.font.SysFont(None, 36)
                restart_text = restart_font.render("Press R to restart", True, WHITE)
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    mixer.quit()

if __name__ == "__main__":
    main()
# This code is a simple implementation of an advanced Bomberman game using Pygame.
# It includes player movement, bomb placement, enemy AI, power-ups, and level progression.
# The game features a grid-based layout with unbreakable and breakable walls, and it supports multiple levels with increasing difficulty.
# Sound effects and animations are included to enhance the gameplay experience.
# The game can be restarted or progressed to the next level using keyboard inputs.
# Note: Replace the placeholder image and sound loading functions with actual files for a complete game experience.
# The game is designed to be played with the arrow keys for movement and spacebar for placing bombs.
# The game ends when the player runs out of lives, and it can be restarted or continued to the next level.
# The player can collect power-ups to enhance their abilities, such as increasing bomb limit, range, or speed.
# Enemies have different types and behaviors, making the game more challenging as levels progress.
# The game is structured to allow for easy expansion, such as adding new enemy types, power-ups, or levels.

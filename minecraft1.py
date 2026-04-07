import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
# import noise
import math
import json
import os
from collections import defaultdict
from itertools import product

# Initialize pygame
pygame.init()
display = (1200, 800)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Enhanced Minecraft-like")

# Enable depth testing and texture 2D
glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Set up OpenGL perspective
gluPerspective(60, (display[0] / display[1]), 0.1, 1000.0)

# Game constants
CHUNK_SIZE = 16
RENDER_DISTANCE = 8
SEA_LEVEL = 62
WORLD_HEIGHT = 256
DAY_LENGTH = 1200  # seconds

# Block types with textures and properties
BLOCKS = {
    "air": {"texture": None, "transparent": True, "solid": False},
    "grass": {"texture": {"top": "grass_top", "side": "grass_side", "bottom": "dirt"}, 
             "transparent": False, "solid": True},
    "dirt": {"texture": "dirt", "transparent": False, "solid": True},
    "stone": {"texture": "stone", "transparent": False, "solid": True},
    "sand": {"texture": "sand", "transparent": False, "solid": True},
    "water": {"texture": "water", "transparent": True, "solid": False, "fluid": True},
    "wood": {"texture": {"top": "wood_top", "side": "wood_side"}, "transparent": False, "solid": True},
    "leaf": {"texture": "leaf", "transparent": True, "solid": True},
    "plank": {"texture": "plank", "transparent": False, "solid": True},
    "glass": {"texture": "glass", "transparent": True, "solid": True},
    "coal_ore": {"texture": "coal_ore", "transparent": False, "solid": True},
    "iron_ore": {"texture": "iron_ore", "transparent": False, "solid": True},
    "crafting_table": {"texture": {"top": "crafting_table_top", "side": "crafting_table_side", 
                                 "bottom": "plank"}, "transparent": False, "solid": True},
    "furnace": {"texture": {"side": "furnace_side", "front": "furnace_front", "top": "furnace_top"}, 
               "transparent": False, "solid": True}
}

# Crafting recipes
CRAFTING_RECIPES = {
    "plank": {"recipe": [["wood"]], "output": 4},
    "stick": {"recipe": [["plank"], ["plank"]], "output": 4},
    "crafting_table": {"recipe": [["plank", "plank"], ["plank", "plank"]], "output": 1},
    "furnace": {"recipe": [["stone", "stone", "stone"], ["stone", None, "stone"], 
                          ["stone", "stone", "stone"]], "output": 1}
}

# Items that can be in inventory
ITEMS = list(BLOCKS.keys()) + ["stick", "coal", "iron_ingot"]
ITEMS.remove("air")

# Mob types
MOBS = {
    "zombie": {"health": 20, "damage": 3, "speed": 0.02, "texture": "zombie"},
    "skeleton": {"health": 15, "damage": 2, "speed": 0.03, "texture": "skeleton"},
    "cow": {"health": 10, "damage": 0, "speed": 0.015, "texture": "cow", "drops": [("leather", 0.5), ("beef", 1)]}
}

# Biome types
BIOMES = {
    "plains": {"height_range": (SEA_LEVEL-2, SEA_LEVEL+4), "blocks": {"top": "grass", "middle": "dirt", "bottom": "stone"}, 
              "trees": 0.02, "decorations": {"flower": 0.01, "tall_grass": 0.05}},
    "desert": {"height_range": (SEA_LEVEL-4, SEA_LEVEL+2), "blocks": {"top": "sand", "middle": "sand", "bottom": "sandstone"}, 
              "trees": 0.001, "decorations": {"dead_bush": 0.01, "cactus": 0.005}},
    "forest": {"height_range": (SEA_LEVEL-1, SEA_LEVEL+6), "blocks": {"top": "grass", "middle": "dirt", "bottom": "stone"}, 
              "trees": 0.05, "decorations": {"flower": 0.03, "mushroom": 0.01}}
}

# Texture loader
def load_textures():
    textures = {}
    # This would load actual texture files in a real implementation
    # For this example, we'll just create colored textures
    for block in BLOCKS.values():
        if isinstance(block["texture"], dict):
            for side in block["texture"].values():
                if side not in textures:
                    textures[side] = glGenTextures(1)
        elif block["texture"] is not None and block["texture"] not in textures:
            textures[block["texture"]] = glGenTextures(1)
    
    for mob in MOBS.values():
        if mob["texture"] not in textures:
            textures[mob["texture"]] = glGenTextures(1)
    
    return textures

textures = load_textures()

class Inventory:
    def __init__(self, size=36):
        self.size = size
        self.slots = [{"item": None, "count": 0} for _ in range(size)]
        self.selected = 0
    
    def add_item(self, item, count=1):
        # First try to stack with existing items
        for slot in self.slots:
            if slot["item"] == item and slot["count"] < 64:
                add = min(count, 64 - slot["count"])
                slot["count"] += add
                count -= add
                if count == 0:
                    return True
        
        # Then try empty slots
        for slot in self.slots:
            if slot["item"] is None and count > 0:
                slot["item"] = item
                add = min(count, 64)
                slot["count"] = add
                count -= add
        
        return count == 0
    
    def remove_item(self, item, count=1):
        for slot in self.slots:
            if slot["item"] == item:
                remove = min(count, slot["count"])
                slot["count"] -= remove
                count -= remove
                if slot["count"] == 0:
                    slot["item"] = None
                if count == 0:
                    return True
        return False
    
    def get_selected_item(self):
        return self.slots[self.selected]["item"]
    
    def draw(self):
        # Draw inventory UI (simplified)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, display[0], display[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Draw hotbar
        hotbar_width = 9 * 40
        glColor4f(0.2, 0.2, 0.2, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(display[0]//2 - hotbar_width//2 - 5, display[1] - 50)
        glVertex2f(display[0]//2 + hotbar_width//2 + 5, display[1] - 50)
        glVertex2f(display[0]//2 + hotbar_width//2 + 5, display[1] - 5)
        glVertex2f(display[0]//2 - hotbar_width//2 - 5, display[1] - 5)
        glEnd()
        
        # Draw slots
        for i in range(9):
            x = display[0]//2 - hotbar_width//2 + i * 40
            y = display[1] - 45
            
            # Slot background
            glColor4f(0.4, 0.4, 0.4, 0.8)
            glBegin(GL_QUADS)
            glVertex2f(x, y)
            glVertex2f(x + 36, y)
            glVertex2f(x + 36, y + 36)
            glVertex2f(x, y + 36)
            glEnd()
            
            # Selected slot highlight
            if i == self.selected:
                glColor4f(1, 1, 1, 0.5)
                glBegin(GL_LINE_LOOP)
                glVertex2f(x-2, y-2)
                glVertex2f(x + 38, y-2)
                glVertex2f(x + 38, y + 38)
                glVertex2f(x-2, y + 38)
                glEnd()
            
            # Item
            slot = self.slots[i]
            if slot["item"] is not None:
                # Draw item texture (simplified)
                glColor4f(*random.choice([(1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1)]))
                glBegin(GL_QUADS)
                glVertex2f(x + 4, y + 4)
                glVertex2f(x + 32, y + 4)
                glVertex2f(x + 32, y + 32)
                glVertex2f(x + 4, y + 32)
                glEnd()
                
                # Draw count
                glColor4f(1, 1, 1, 1)
                glRasterPos2f(x + 24, y + 24)
                for c in str(slot["count"]):
                    pygame.glyph.render(c)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)

class CraftingSystem:
    def __init__(self, inventory):
        self.inventory = inventory
        self.recipes = CRAFTING_RECIPES
        self.grid = [[None for _ in range(3)] for _ in range(3)]
    
    def can_craft(self, item):
        if item not in self.recipes:
            return False
        
        recipe = self.recipes[item]["recipe"]
        # Check if the crafting grid matches any recipe variation
        for rotation in [0, 90, 180, 270]:
            rotated = self.rotate_grid(rotation)
            if self.matches_recipe(rotated, recipe):
                return True
        return False
    
    def matches_recipe(self, grid, recipe):
        for i in range(3):
            for j in range(3):
                if (i >= len(recipe) or (j >= len(recipe[i])) or (grid[i][j] != recipe[i][j])):
                    return False
        return True
    
    def rotate_grid(self, degrees):
        rotated = [[None for _ in range(3)] for _ in range(3)]
        if degrees == 0:
            return self.grid
        elif degrees == 90:
            for i in range(3):
                for j in range(3):
                    rotated[j][2-i] = self.grid[i][j]
        elif degrees == 180:
            for i in range(3):
                for j in range(3):
                    rotated[2-i][2-j] = self.grid[i][j]
        elif degrees == 270:
            for i in range(3):
                for j in range(3):
                    rotated[2-j][i] = self.grid[i][j]
        return rotated
    
    def craft(self, item):
        if not self.can_craft(item):
            return False
        
        recipe = self.recipes[item]["recipe"]
        output = self.recipes[item]["output"]
        
        # Remove ingredients
        for i in range(len(recipe)):
            for j in range(len(recipe[i])):
                if recipe[i][j] is not None:
                    self.inventory.remove_item(recipe[i][j])
        
        # Add output
        return self.inventory.add_item(item, output)

class Mob:
    def __init__(self, mob_type, x, y, z):
        self.type = mob_type
        self.x = x
        self.y = y
        self.z = z
        self.health = MOBS[mob_type]["health"]
        self.speed = MOBS[mob_type]["speed"]
        self.target = None
        self.attack_cooldown = 0
    
    def update(self, world, player_pos):
        px, py, pz = player_pos
        
        # Simple AI
        if self.type in ["zombie", "skeleton"]:  # Hostile mobs
            # Move toward player if within 16 blocks
            distance = math.sqrt((self.x - px)**2 + (self.y - py)**2 + (self.z - pz)**2)
            if distance < 16:
                dx = (px - self.x) / distance * self.speed
                dz = (pz - self.z) / distance * self.speed
                
                # Simple pathfinding - check if path is clear
                new_x = self.x + dx
                new_z = self.z + dz
                
                if world.get_block(int(new_x), int(self.y), int(new_z)) == "air":
                    self.x = new_x
                    self.z = new_z
                
                # Attack if close enough
                if distance < 2 and self.attack_cooldown <= 0:
                    # Damage player
                    self.attack_cooldown = 20  # 1 second cooldown
                    return MOBS[self.type]["damage"]
        
        elif self.type == "cow":  # Passive mob
            # Random wandering
            if random.random() < 0.02:
                self.x += random.uniform(-self.speed, self.speed)
                self.z += random.uniform(-self.speed, self.speed)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        return 0
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        # Draw mob (simplified as a colored cube)
        glColor3f(*random.choice([(1,0,0), (0,1,0), (0,0,1)]))
        glBegin(GL_QUADS)
        for face in [(0,1,2,3), (4,5,6,7), (0,1,5,4), 
                    (2,3,7,6), (0,3,7,4), (1,2,6,5)]:
            for vertex in face:
                glVertex3fv(self.cube_vertices[vertex])
        glEnd()
        
        glPopMatrix()
    
    @property
    def cube_vertices(self):
        return [
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5]
        ]

class World:
    def __init__(self):
        self.chunks = {}
        self.active_chunks = set()
        self.mobs = []
        self.time = 0  # 0-24000 (Minecraft time)
        self.weather = "clear"  # "clear", "rain", "thunder"
        self.spawn_point = (0, SEA_LEVEL + 2, 0)
        
        # Generate spawn chunks
        self.generate_chunk(0, 0)
    
    def get_chunk_key(self, x, z):
        return (x // CHUNK_SIZE, z // CHUNK_SIZE)
    
    def generate_chunk(self, cx, cz):
        key = (cx, cz)
        if key in self.chunks:
            return
        
        chunk_data = {}
        biome = random.choice(list(BIOMES.keys()))
        biome_data = BIOMES[biome]
        
        for x in range(cx * CHUNK_SIZE, (cx + 1) * CHUNK_SIZE):
            for z in range(cz * CHUNK_SIZE, (cz + 1) * CHUNK_SIZE):
                # Generate height using Perlin noise
                # height = int(noise.pnoise2(x * 0.1, z * 0.1, octaves=4) * 10 + SEA_LEVEL)
                height = max(1, min(height, WORLD_HEIGHT - 10))
                
                # Generate layers based on biome
                for y in range(WORLD_HEIGHT):
                    if y > height:
                        if y <= SEA_LEVEL:
                            chunk_data[(x, y, z)] = "water"
                        else:
                            chunk_data[(x, y, z)] = "air"
                    elif y == height:
                        chunk_data[(x, y, z)] = biome_data["blocks"]["top"]
                    elif y > height - 4:
                        chunk_data[(x, y, z)] = biome_data["blocks"]["middle"]
                    else:
                        chunk_data[(x, y, z)] = biome_data["blocks"]["bottom"]
                
                # Generate trees
                if (biome_data["trees"] > 0 and random.random() < biome_data["trees"] 
                    and height > SEA_LEVEL and chunk_data[(x, height, z)] == biome_data["blocks"]["top"]):
                    tree_height = random.randint(4, 6)
                    for ty in range(height + 1, height + tree_height + 1):
                        chunk_data[(x, ty, z)] = "wood"
                    
                    # Generate leaves
                    for tx in range(x - 2, x + 3):
                        for tz in range(z - 2, z + 3):
                            for ty in range(height + tree_height - 1, height + tree_height + 2):
                                if (tx, ty, tz) not in chunk_data or chunk_data[(tx, ty, tz)] == "air":
                                    chunk_data[(tx, ty, tz)] = "leaf"
                
                # Generate ores
                if y < SEA_LEVEL - 10 and random.random() < 0.02:
                    vein_size = random.randint(3, 8)
                    ore_type = "coal_ore" if random.random() < 0.7 else "iron_ore"
                    for dx in range(-vein_size//2, vein_size//2 + 1):
                        for dy in range(-vein_size//2, vein_size//2 + 1):
                            for dz in range(-vein_size//2, vein_size//2 + 1):
                                nx, ny, nz = x + dx, y + dy, z + dz
                                if (nx, ny, nz) in chunk_data and chunk_data[(nx, ny, nz)] == "stone":
                                    chunk_data[(nx, ny, nz)] = ore_type
        
        self.chunks[key] = chunk_data
        
        # Spawn mobs in this chunk
        if random.random() < 0.3:  # 30% chance to spawn mobs in a chunk
            mob_type = random.choice(list(MOBS.keys()))
            for _ in range(random.randint(1, 3)):
                x = random.randint(cx * CHUNK_SIZE, (cx + 1) * CHUNK_SIZE - 1)
                z = random.randint(cz * CHUNK_SIZE, (cz + 1) * CHUNK_SIZE - 1)
                y = self.get_height_at(x, z) + 1
                if y > SEA_LEVEL:
                    self.mobs.append(Mob(mob_type, x, y, z))
    
    def get_height_at(self, x, z):
        # Find the highest non-air block at this x,z
        for y in range(WORLD_HEIGHT - 1, -1, -1):
            if self.get_block(x, y, z) != "air":
                return y
        return 0
    
    def get_block(self, x, y, z):
        chunk_key = self.get_chunk_key(x, z)
        if chunk_key in self.chunks:
            return self.chunks[chunk_key].get((x, y, z), "air")
        return "air"
    
    def set_block(self, x, y, z, block_type):
        chunk_key = self.get_chunk_key(x, z)
        if chunk_key in self.chunks:
            self.chunks[chunk_key][(x, y, z)] = block_type
    
    def update_chunks(self, player_pos):
        px, _, pz = player_pos
        current_chunk = self.get_chunk_key(px, pz)
        
        # Unload distant chunks
        to_unload = []
        for chunk in self.chunks:
            if abs(chunk[0] - current_chunk[0]) > RENDER_DISTANCE or abs(chunk[1] - current_chunk[1]) > RENDER_DISTANCE:
                to_unload.append(chunk)
        
        for chunk in to_unload:
            del self.chunks[chunk]
        
        # Load nearby chunks
        for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
                cx = current_chunk[0] + dx
                cz = current_chunk[1] + dz
                if (cx, cz) not in self.chunks:
                    self.generate_chunk(cx, cz)
        
        # Update mobs
        player_damage = 0
        for mob in self.mobs[:]:
            damage = mob.update(self, player_pos)
            if damage > 0:
                player_damage += damage
            
            # Remove dead mobs
            if mob.health <= 0:
                self.mobs.remove(mob)
                # Drop items
                if mob.type in MOBS and "drops" in MOBS[mob.type]:
                    for item, chance in MOBS[mob.type]["drops"]:
                        if random.random() < chance:
                            # In a real game, we'd create an item entity here
                            pass
        
        return player_damage
    
    def update_time(self):
        self.time = (self.time + 1) % 24000
        # Change weather occasionally
        if random.random() < 0.0005:
            self.weather = random.choice(["clear", "rain", "thunder"])
    
    def get_light_level(self, x, y, z):
        # Simplified daylight cycle
        is_day = 0 < self.time < 12000
        sky_light = max(0, min(15, int(15 * (1 - abs(self.time - 6000) / 6000))))
        
        # Block light (torches, etc.) would be added here
        block_light = 0
        
        return max(sky_light, block_light)
    
    def save(self, filename):
        data = {
            "chunks": {f"{k[0]},{k[1]}": v for k, v in self.chunks.items()},
            "time": self.time,
            "weather": self.weather,
            "spawn_point": self.spawn_point
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.chunks = {tuple(map(int, k.split(','))): v for k, v in data["chunks"].items()}
                self.time = data["time"]
                self.weather = data.get("weather", "clear")
                self.spawn_point = data.get("spawn_point", (0, SEA_LEVEL + 2, 0))

class Player:
    def __init__(self, world):
        self.world = world
        self.x, self.y, self.z = world.spawn_point
        self.rotation_x = 0
        self.rotation_y = 0
        self.health = 20
        self.hunger = 20
        self.inventory = Inventory()
        self.crafting = CraftingSystem(self.inventory)
        self.flying = False
        self.velocity_y = 0
        self.on_ground = False
        
        # Starting items
        self.inventory.add_item("plank", 32)
        self.inventory.add_item("stick", 16)
        self.inventory.add_item("dirt", 64)
    
    def update_position(self):
        keys = pygame.key.get_pressed()
        mouse_rel = pygame.mouse.get_rel()
        
        # Mouse look
        self.rotation_x += mouse_rel[0] * 0.2
        self.rotation_y -= mouse_rel[1] * 0.2
        self.rotation_y = max(-90, min(90, self.rotation_y))
        
        # Movement
        move_speed = 0.1 if keys[K_LSHIFT] else 0.05
        if self.flying:
            move_speed *= 3
        
        rot_y_rad = math.radians(self.rotation_x)
        
        if keys[K_w]:
            self.x -= math.sin(rot_y_rad) * move_speed
            self.z -= math.cos(rot_y_rad) * move_speed
        if keys[K_s]:
            self.x += math.sin(rot_y_rad) * move_speed
            self.z += math.cos(rot_y_rad) * move_speed
        if keys[K_a]:
            self.x -= math.cos(rot_y_rad) * move_speed
            self.z += math.sin(rot_y_rad) * move_speed
        if keys[K_d]:
            self.x += math.cos(rot_y_rad) * move_speed
            self.z -= math.sin(rot_y_rad) * move_speed
        
        # Jumping/flying
        if keys[K_SPACE]:
            if self.flying:
                self.y += move_speed
            elif self.on_ground:
                self.velocity_y = 0.15
        
        # Sneaking/descending
        if keys[K_LCTRL]:
            if self.flying:
                self.y -= move_speed
            else:
                # Sneak - would be implemented in a real game
                pass
        
        # Gravity
        if not self.flying:
            self.velocity_y -= 0.005  # Gravity
            self.y += self.velocity_y
            
            # Collision detection
            self.on_ground = False
            block_below = self.world.get_block(int(self.x), int(self.y - 0.5), int(self.z))
            if block_below != "air" and block_below != "water":
                self.y = int(self.y) + 0.5
                self.velocity_y = 0
                self.on_ground = True
            
            # Check if landed in water
            if block_below == "water":
                self.velocity_y *= 0.5  # Water resistance
                if self.velocity_y < -0.02:
                    self.velocity_y = -0.02
        
        # Collision with blocks
        for dy in [0, 1, 2]:  # Check at feet, waist, and head level
            y_pos = int(self.y + dy)
            block = self.world.get_block(int(self.x), y_pos, int(self.z))
            if block != "air" and block != "water":
                # Push player out of the block
                self.x = int(self.x) + 0.5
                self.z = int(self.z) + 0.5
        
        # World boundaries
        self.x = max(0, min(WORLD_HEIGHT * CHUNK_SIZE - 1, self.x))
        self.z = max(0, min(WORLD_HEIGHT * CHUNK_SIZE - 1, self.z))
        self.y = max(0, min(WORLD_HEIGHT - 1, self.y))
    
    def raycast(self, max_distance=10):
        rot_x_rad = math.radians(self.rotation_y)
        rot_y_rad = math.radians(self.rotation_x)
        
        # Calculate ray direction
        dx = -math.sin(rot_y_rad) * math.cos(rot_x_rad)
        dy = -math.sin(rot_x_rad)
        dz = -math.cos(rot_y_rad) * math.cos(rot_x_rad)
        
        step = 0.1
        distance = 0
        
        while distance < max_distance:
            distance += step
            x = self.x + dx * distance
            y = self.y + 1.6 + dy * distance  # 1.6 is roughly eye level
            z = self.z + dz * distance
            
            block = self.world.get_block(int(x), int(y), int(z))
            if block != "air":
                return (int(x), int(y), int(z)), block
        
        return None, None
    
    def draw_crosshair(self):
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, display[0], display[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        glVertex2f(display[0]//2 - 10, display[1]//2)
        glVertex2f(display[0]//2 + 10, display[1]//2)
        glVertex2f(display[0]//2, display[1]//2 - 10)
        glVertex2f(display[0]//2, display[1]//2 + 10)
        glEnd()
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
    
    def draw_hud(self):
        # Health and hunger bars
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, display[0], display[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Health
        for i in range(10):
            x = 20 + i * 20
            y = 20
            if self.health > i * 2:
                glColor3f(1, 0, 0)
                glBegin(GL_QUADS)
                glVertex2f(x, y)
                glVertex2f(x + 16, y)
                glVertex2f(x + 16, y + 8)
                glVertex2f(x, y + 8)
                glEnd()
        
        # Hunger
        for i in range(10):
            x = 20 + i * 20
            y = 35
            if self.hunger > i * 2:
                glColor3f(1, 0.8, 0)
                glBegin(GL_QUADS)
                glVertex2f(x, y)
                glVertex2f(x + 16, y)
                glVertex2f(x + 16, y + 8)
                glVertex2f(x, y + 8)
                glEnd()
        
        # Time of day indicator
        time_x = display[0] - 120
        time_y = 20
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(time_x, time_y)
        glVertex2f(time_x + 100, time_y)
        glVertex2f(time_x + 100, time_y + 10)
        glVertex2f(time_x, time_y + 10)
        glEnd()
        
        day_progress = self.world.time / 24000
        sun_x = time_x + day_progress * 100
        is_day = 0 < self.world.time < 12000
        glColor3f(1, 1, 0) if is_day else glColor3f(0.8, 0.8, 1)
        glBegin(GL_QUADS)
        glVertex2f(sun_x - 5, time_y - 5)
        glVertex2f(sun_x + 5, time_y - 5)
        glVertex2f(sun_x + 5, time_y + 15)
        glVertex2f(sun_x - 5, time_y + 15)
        glEnd()
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)

def render_block(x, y, z, block_type):
    if block_type == "air":
        return
    
    block_data = BLOCKS[block_type]
    
    # Get texture(s)
    if isinstance(block_data["texture"], dict):
        top_tex = block_data["texture"].get("top", block_data["texture"].get("side"))
        side_tex = block_data["texture"].get("side")
        bottom_tex = block_data["texture"].get("bottom", block_data["texture"].get("side"))
    else:
        top_tex = side_tex = bottom_tex = block_data["texture"]
    
    # Vertices for a cube
    vertices = [
        [x, y, z],
        [x+1, y, z],
        [x+1, y+1, z],
        [x, y+1, z],
        [x, y, z+1],
        [x+1, y, z+1],
        [x+1, y+1, z+1],
        [x, y+1, z+1]
    ]
    
    faces = [
        (0,1,2,3),  # Front
        (4,5,6,7),  # Back
        (0,1,5,4),  # Bottom
        (2,3,7,6),  # Top
        (0,3,7,4),  # Left
        (1,2,6,5)   # Right
    ]
    
    face_textures = [side_tex, side_tex, bottom_tex, top_tex, side_tex, side_tex]
    
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        tex = face_textures[i]
        if tex is None:
            continue
            
        # In a real game, we'd bind the actual texture here
        # For this example, we'll just use colors
        if tex == "grass_top":
            glColor3f(0.2, 0.8, 0.2)
        elif tex == "grass_side":
            glColor3f(0.5, 0.35, 0.05)
        elif tex == "dirt":
            glColor3f(0.5, 0.35, 0.05)
        elif tex == "stone":
            glColor3f(0.5, 0.5, 0.5)
        elif tex == "water":
            glColor4f(0.2, 0.2, 0.8, 0.7)
        else:
            glColor3f(0.8, 0.8, 0.8)
        
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def render_world(world, player_pos):
    px, py, pz = player_pos
    
    # Calculate visible chunks
    visible_chunks = set()
    for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
        for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            cx = int(px) // CHUNK_SIZE + dx
            cz = int(pz) // CHUNK_SIZE + dz
            visible_chunks.add((cx, cz))
    
    # Draw sky (simplified)
    glClearColor(0.53, 0.81, 0.92, 1)  # Sky blue
    
    # Draw blocks
    for chunk in visible_chunks:
        if chunk in world.chunks:
            for (x, y, z), block_type in world.chunks[chunk].items():
                # Only render blocks near the player
                if (abs(x - px) < RENDER_DISTANCE * CHUNK_SIZE and 
                    abs(z - pz) < RENDER_DISTANCE * CHUNK_SIZE and 
                    abs(y - py) < RENDER_DISTANCE * CHUNK_SIZE):
                    render_block(x, y, z, block_type)
    
    # Draw mobs
    for mob in world.mobs:
        mob.draw()

def main():
    world = World()
    player = Player(world)
    
    # Load saved world if exists
    world.load("world.json")
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F:
                    player.flying = not player.flying
                elif event.key == pygame.K_e:
                    # Open inventory/crafting (simplified)
                    pass
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                block_pos, block_type = player.raycast()
                if block_pos:
                    if event.button == 1:  # Left click - break block
                        world.set_block(*block_pos, "air")
                    elif event.button == 3:  # Right click - place block
                        selected_item = player.inventory.get_selected_item()
                        if selected_item in BLOCKS:
                            # Calculate adjacent position
                            x, y, z = block_pos
                            px, py, pz = player.x, player.y + 1.6, player.z
                            
                            # Determine which face was clicked
                            if abs(block_pos[0] - px) > abs(block_pos[2] - pz):
                                adj_x = x + (1 if px > x else -1)
                                adj_pos = (adj_x, y, z)
                            else:
                                adj_z = z + (1 if pz > z else -1)
                                adj_pos = (x, y, adj_z)
                            
                            # Place block if position is air and we have the item
                            if world.get_block(*adj_pos) == "air":
                                if player.inventory.remove_item(selected_item):
                                    world.set_block(*adj_pos, selected_item)
        
        # Update game state
        player.update_position()
        damage = world.update_chunks((player.x, player.y, player.z))
        player.health -= damage
        world.update_time()
        
        # Regenerate health if well-fed
        if player.hunger > 18 and player.health < 20 and random.random() < 0.01:
            player.health += 1
        
        # Decrease hunger over time
        if random.random() < 0.001:
            player.hunger = max(0, player.hunger - 1)
        
        # Check if player died
        if player.health <= 0:
            player.health = 20
            player.hunger = 20
            player.x, player.y, player.z = world.spawn_point
        
        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set up camera
        glLoadIdentity()
        rot_x_rad = math.radians(player.rotation_y)
        rot_y_rad = math.radians(player.rotation_x)
        
        # Calculate camera position (eye level at 1.6 units)
        eye_x = player.x
        eye_y = player.y + 1.6
        eye_z = player.z
        
        # Calculate look-at point
        look_x = eye_x - math.sin(rot_y_rad) * math.cos(rot_x_rad)
        look_y = eye_y - math.sin(rot_x_rad)
        look_z = eye_z - math.cos(rot_y_rad) * math.cos(rot_x_rad)
        
        gluLookAt(
            eye_x, eye_y, eye_z,
            look_x, look_y, look_z,
            0, 1, 0
        )
        
        # Render world
        render_world(world, (player.x, player.y, player.z))
        
        # Draw HUD
        player.draw_crosshair()
        player.draw_hud()
        player.inventory.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    # Save world before exiting
    world.save("world.json")
    pygame.quit()

if __name__ == "__main__":
    main() 
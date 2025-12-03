"""
    Project: Disciples Of The Truth (Christian 2D RPG)
    Author: Aaron Keith Sanders
    Date: 24 October 2025
    File: graphics.py
"""
import pygame
import random
import physics
from camera import Camera

pygame.init()


class Sprites:
    def __init__(self, image):
        self.spritesheet = image

    def LoadSprite(self, frame, width, height, scale, row):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0),
                   (frame * width, row * height, width, height))
        return pygame.transform.scale(image, (width * scale, height * scale))


class Player(pygame.sprite.Sprite):
    def __init__(self, spritesheet, x, y, frame_width, frame_height, scale):
        super().__init__()
        self.spritesheet = spritesheet
        self.frame_height = frame_height
        self.scale = scale

        # Load animations
        self.animations = {
            "down": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 0) for i in range(4)],
            "right": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 1) for i in range(4)],
            "left": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 2) for i in range(4)],
            "up": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 3) for i in range(4)],
        }

        self.direction = "down"
        self.image = self.animations["down"][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.frame_index = 0
        self.animation_speed = 6  # frames per second
        self.speed = 150.0        # pixels per second

    def update(self, keys, camera, dt):
        dx, dy = 0, 0
        moving = False

        # Movement
        if keys[pygame.K_LEFT]:
            dx -= 1
            self.direction = "left"
            moving = True
        if keys[pygame.K_RIGHT]:
            dx += 1
            self.direction = "right"
            moving = True
        if keys[pygame.K_UP]:
            dy -= 1
            self.direction = "up"
            moving = True
        if keys[pygame.K_DOWN]:
            dy += 1
            self.direction = "down"
            moving = True

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        # Apply dt-based movement
        self.pos_x += dx * self.speed * dt
        self.pos_y += dy * self.speed * dt
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        # Animation update
        if moving:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = self.animations[self.direction][int(self.frame_index)]


class NPC(pygame.sprite.Sprite):
    def __init__(self, spritesheet, x, y, frame_width, frame_height, scale, chartype):
        super().__init__()
        self.spritesheet = spritesheet

        # Animations
        self.animations = {
            "down": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 0) for i in range(4)],
            "right": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 1) for i in range(4)],
            "left": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 2) for i in range(4)],
            "up": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 3) for i in range(4)],
        }

        self.direction = "down"
        self.image = self.animations["down"][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.dx = 0
        self.dy = 0

        self.frame_index = 0
        self.animation_speed = 6     # frames per second
        self.speed = 60.0            # pixels per second
        self.move_timer = 0
        self.move_interval = 1.0

    def choose_new_direction(self):
        direction = random.choice(["up", "down", "left", "right", "none"])

        if direction == "left":
            self.dx, self.dy = -1, 0
            self.direction = "left"
        elif direction == "right":
            self.dx, self.dy = 1, 0
            self.direction = "right"
        elif direction == "up":
            self.dx, self.dy = 0, -1
            self.direction = "up"
        elif direction == "down":
            self.dx, self.dy = 0, 1
            self.direction = "down"
        else:
            # Idle keeps current direction
            self.dx, self.dy = 0, 0

    def update(self, roaming, dt):
        self.move_timer += dt

        if roaming and self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move_interval = random.uniform(1.0, 3.0)
            self.choose_new_direction()

        # Movement
        self.pos_x += self.dx * self.speed * dt
        self.pos_y += self.dy * self.speed * dt
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        # Animation
        if roaming and (self.dx != 0 or self.dy != 0):
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = self.animations[self.direction][int(self.frame_index)]


class TileInstance:
    """Represents a single tile in the world"""

    def __init__(self, x, y, width, height, image, physics_world=None, debug_collider=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

        # Add collider if a physics world is provided
        self.collider = None
        if physics_world:
            self.collider = physics.BoxCollider(x, y, width, height)
            self.collider.enable_debug(debug_collider)
            physics_world.add_collider(self.collider)

    def draw(self, surface, camera: Camera):
        # Draw the tile
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen_rect = camera.apply(rect)
        surface.blit(self.image, screen_rect)

        # Draw debug collider if enabled
        if self.collider and self.collider.debug:
            pygame.draw.rect(surface, (255, 0, 0), screen_rect, 1)


class Tiles:
    """Responsible for creating and managing tile instances"""

    def __init__(self, tileset_image, physics_world=None, has_physics=True, debug_collider=True):
        self.tileset = tileset_image
        self.physics_world = physics_world if has_physics else None
        self.debug_collider = debug_collider

    def LoadTile(self, frame, width, height, scale, row):
        """Extract and scale a tile from the tileset"""
        tile = pygame.Surface((width, height), pygame.SRCALPHA)
        tile.blit(self.tileset, (0, 0), (frame * width, row * height, width, height))
        scaled_w = width * scale
        scaled_h = height * scale
        return pygame.transform.scale(tile, (scaled_w, scaled_h)), scaled_w, scaled_h

    def create_tile(self, x, y, frame, width, height, scale, row):
        """Create a TileInstance with optional physics"""
        tile_image, tw, th = self.LoadTile(frame, width, height, scale, row)
        return TileInstance(
            x=x,
            y=y,
            width=tw,
            height=th,
            image=tile_image,
            physics_world=self.physics_world,
            debug_collider=self.debug_collider
        )

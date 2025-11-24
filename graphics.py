"""
    Project: Disciples Of The Truth (Christian 2D RPG)
    Author: Aaron Keith Sanders
    Date: 24 October 2025
    File: graphics.py
"""
import pygame
import physics
from camera import Camera

pygame.init()


class Sprites:
    """The Sprites class handles loading sprites and spritesheets"""

    def __init__(self, image):
        self.spritesheet = image

    def LoadSprite(self, frame, width, height, scale, row):
        """
            Loads a sprite from a spritesheet based on its x, y and
            its width, height selection
        """
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (frame * width, row * height,
                                              width, height))
        return pygame.transform.scale(image, (width * scale, height * scale))


class Player(pygame.sprite.Sprite):
    """
        The Player class is responsible for handling the player and its animations, movement, etc.
    """

    def __init__(self, spritesheet, x, y, frame_width, frame_height, scale):
        super().__init__()
        self.spritesheet = spritesheet
        self.frame_height = frame_height
        self.scale = scale
        self.animations = None
        self.image = None
        self.direction = "down"

        # Load animations
        self.animations = {
            "down": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 0) for i in range(4)],
            "right": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 1) for i in range(4)],
            "left": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 2) for i in range(4)],
            "up": [self.spritesheet.LoadSprite(i, frame_width, frame_height, scale, 3) for i in range(4)],
        }

        self.image = self.animations["down"][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.speed = 3.0

    def update(self, keys, camera):
        dx, dy = 0, 0
        moving = False

        # Movement input
        if keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direction = "left"
            moving = True
        if keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direction = "right"
            moving = True
        if keys[pygame.K_UP]:
            dy -= self.speed
            self.direction = "up"
            moving = True
        if keys[pygame.K_DOWN]:
            dy += self.speed
            self.direction = "down"
            moving = True

        # Camera zoom controls
        if keys[pygame.K_q]:
            camera.zoom_in()
        if keys[pygame.K_e]:
            camera.zoom_out()

        # Apply movement
        self.pos_x += dx
        self.rect.x = int(self.pos_x)
        self.pos_y += dy
        self.rect.y = int(self.pos_y)

        # Update animation
        if moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = self.animations[self.direction][int(self.frame_index)]


class Tiles:
    """
    The Tiles class handles loading tiles from a tileset, optionally creating
    physics colliders and drawing visual debug colliders.
    """

    def __init__(self, image, physics_world, has_physics=True, debug_collider=True):
        """
        image : pygame.Surface (tileset)
        has_physics : bool — will or will not contain a physics collider
        debug_collider : bool - debug_colliders are either red for testing or transparent for tested
        """
        self.tileset = image
        self.has_physics = has_physics
        self.debug_collider = debug_collider
        self.tile_physics = physics_world

    def set_collider_visible(self, visible: bool):
        """
        Turn collider debug visibility ON (red) or OFF (transparent).
        """
        self.debug_collider = visible

    def enable_physics(self, enabled: bool):
        """
        Turn physics colliders on or off.
        """
        self.has_physics = enabled

    def LoadTile(self, frame, width, height, scale, row):
        """
        Extract a tile from the tileset and return a scaled surface.
        """

        # Extract original tile
        tile = pygame.Surface((width, height), pygame.SRCALPHA)
        tile.blit(self.tileset, (0, 0), (frame * width, row * height, width, height))

        # Scale the tile
        scaled_w = width * scale
        scaled_h = height * scale

        tile = pygame.transform.scale(tile, (scaled_w, scaled_h))

        return tile, scaled_w, scaled_h

    def blit_tile(self, surface, x, y, frame, width, height, scale, row, color=(255, 0, 0)):
        """
        Draw a tile to the screen. Apply collider if enabled.
        """

        # load tile surface
        tile, tw, th = self.LoadTile(frame, width, height, scale, row)
        surface.blit(tile, (x, y))

        # apply colliders if physics is enabled
        if self.has_physics:
            self._apply_collider(x, y, tw, th, surface, color)

        return tile

    def _apply_collider(self, x, y, width, height, surface, color):
        """
        Create a physics collider matching the tile and draw a debug collider
        (either red or invisible).
        """

        collider = physics.BoxCollider(x, y, width, height)
        collider.enable_debug(self.debug_collider)
        self.tile_physics.add_collider(collider)

        if self.debug_collider:
            pygame.draw.rect(surface, color, (x, y, width, height), 1)
        else:
            # Transparent physics collder
            pass

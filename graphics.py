"""
    Project: Disciples Of The Truth (Christian 2D RPG)
    Author: Aaron Keith Sanders
    Date: 24 October 2025
    File: graphics.py
"""
import pygame

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

        # Animation lists (rows: down=0, left=1, right=2, up=3)
        self.animations = {
            "down": [self.spritesheet.LoadSprite(i, frame_width, frame_height,
                                                 scale, 0) for i in range(4)],
            "right": [self.spritesheet.LoadSprite(i, frame_width, frame_height,
                                                  scale, 1) for i in range(4)],
            "left": [self.spritesheet.LoadSprite(i, frame_width, frame_height,
                                                 scale, 2) for i in range(4)],
            "up": [self.spritesheet.LoadSprite(i, frame_width, frame_height,
                                               scale, 3) for i in range(4)],
        }

        self.image = self.animations["down"][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Keep float positions for smoother movement
        self.pos_x = float(x)
        self.pos_y = float(y)

        # Animation control
        self.frame_index = 0
        self.animation_speed = 0.15  # much faster

        # Movement
        self.speed = 3.0  # pixels per frame

    def update(self, keys):
        moving = False

        if keys[pygame.K_LEFT]:
            self.pos_x -= self.speed
            self.direction = "left"
            moving = True

        if keys[pygame.K_RIGHT]:
            self.pos_x += self.speed
            self.direction = "right"
            moving = True

        if keys[pygame.K_DOWN]:
            self.pos_y += self.speed
            self.direction = "down"
            moving = True

        if keys[pygame.K_UP]:
            self.pos_y -= self.speed
            self.direction = "up"
            moving = True

        # Update integer rect position from floats
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        # Animation update
        if moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = self.animations[self.direction][int(self.frame_index)]

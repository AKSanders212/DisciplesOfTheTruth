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

    def __init__(self):
        self.path = None
        self.sprite_sheet = None

    def LoadSprite(self, path, rect):
        """
        Loads a specific frame (subsurface) from a sprite sheet.
        :param path: Path to the sprite sheet image
        :param rect: pygame.Rect(x, y, width, height) for the frame to extract
        """
        self.path = path
        self.sprite_sheet = pygame.image.load(self.path).convert_alpha()
        # Extract the specific sprite frame
        frame = self.sprite_sheet.subsurface(rect)
        return frame


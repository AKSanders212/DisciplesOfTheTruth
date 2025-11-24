"""
Project: Disciples Of The Truth (Christian 2D RPG)
Author: Aaron Keith Sanders
Date: 8 November 2025
File: physics.py
"""
import pygame

pygame.init()


class Camera:
    def __init__(self, width, height, zoom=1.0):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.zoom = zoom

    def zoom_in(self):
        if self.zoom < 3:
            self.zoom += 0.1
        return self.zoom

    def zoom_out(self):
        if self.zoom >= 1:
            self.zoom -= 0.1
        return self.zoom

    def apply(self, rect):
        """Convert world rect to screen rect using camera position and zoom."""
        x = (rect.centerx - self.camera_rect.centerx) * self.zoom + self.width // 2
        y = (rect.centery - self.camera_rect.centery) * self.zoom + self.height // 2
        w = rect.width * self.zoom
        h = rect.height * self.zoom
        return pygame.Rect(int(x - w // 2), int(y - h // 2), int(w), int(h))

    def update(self, target):
        """Center camera on target"""
        self.camera_rect.centerx = target.rect.centerx
        self.camera_rect.centery = target.rect.centery

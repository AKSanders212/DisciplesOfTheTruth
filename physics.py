"""
Project: Disciples Of The Truth (Christian 2D RPG)
Author: Aaron Keith Sanders
Date: 8 November 2025
File: physics.py
"""

import pygame

pygame.init()


class BoxCollider:
    """Responsible for handling box collisions"""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, camera=None, color=(255, 0, 0)):
        """For drawing debug based box collisions with a default color of red"""
        draw_rect = self.rect
        if camera:
            draw_rect = camera.apply(self.rect)
        pygame.draw.rect(surface, color, draw_rect, 2)


class Physics:
    """The physics system for the game world"""

    def __init__(self, world_width, world_height):
        self.colliders = []
        self.world_rect = pygame.Rect(0, 0, world_width, world_height)

    def add_collider(self, collider: BoxCollider):
        """Adds a BoxCollider to the array of physics colliders"""
        self.colliders.append(collider)

    def clear_colliders(self):
        """Clears the array of colliders"""
        self.colliders.clear()

    def handle_collisions(self, player):
        """Keeps the player sprite within the game world boundaries and resolves object collisions"""
        if not self.world_rect.contains(player.rect):
            if player.rect.left < self.world_rect.left:
                player.rect.left = self.world_rect.left
            if player.rect.right > self.world_rect.right:
                player.rect.right = self.world_rect.right
            if player.rect.top < self.world_rect.top:
                player.rect.top = self.world_rect.top
            if player.rect.bottom > self.world_rect.bottom:
                player.rect.bottom = self.world_rect.bottom

            # Sync player float positions with regard to the player rect
            player.pos_x, player.pos_y = player.rect.topleft

        # Collide with static walls
        for collider in self.colliders:
            if player.rect.colliderect(collider.rect):
                self.resolve_collision(player, collider)

    def resolve_collision(self, player, collider):
        """Ensure the player is seperated from colliders by smallest overlap"""
        dx = player.rect.centerx - collider.rect.centerx
        dy = player.rect.centery - collider.rect.centery

        # variables that contain where player overlap with colliders occur
        overlap_x = (player.rect.width / 2 + collider.rect.width / 2) - abs(dx)
        overlap_y = (player.rect.height / 2 + collider.rect.height / 2) - abs(dy)

        # Determine which axis to resolve on (smallest overlap first)
        if overlap_x < overlap_y:
            # --- Horizontal collision ---
            if dx > 0:
                # Player hit from the right
                player.rect.left = collider.rect.right
            else:
                # Player hit from the left
                player.rect.right = collider.rect.left

            # Sync X position (prevents teleporting)
            player.pos_x = player.rect.x

        else:
            # --- Vertical collision ---
            if dy > 0:
                # Player hit from below
                player.rect.top = collider.rect.bottom
            else:
                # Player hit from above
                player.rect.bottom = collider.rect.top

            # Sync Y position
            player.pos_y = player.rect.y

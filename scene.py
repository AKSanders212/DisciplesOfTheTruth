"""
Project: Disciples Of The Truth (Christian 2D RPG)
Author: Aaron Keith Sanders
Date: 8 November 2025
File: scene.py
"""

import pygame
import graphics
import camera
import physics
import audio


class Scene:
    """Base class for all game scenes."""

    def __init__(self, screen):
        self.screen = screen
        self.running = True

    def handle_events(self, events):
        """Handle per-frame input events."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, keys):
        """Update scene objects (override in subclass)."""
        pass

    def draw(self):
        """Draw everything to the screen (override in subclass)."""
        pass


class Scene01(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        # --- Core setup ---
        self.surface = pygame.Surface((1600, 1200))
        self.background_color = (100, 200, 100)

        # --- Systems ---
        self.physics = physics.Physics(world_width=1600, world_height=1200)
        self.audio_player = audio.MusicPlayer()
        self.camera = camera.Camera(800, 600, zoom=2.0)

        # --- Player setup ---
        player_image = pygame.image.load("graphics/sprites/male_chr01_sheet.png").convert_alpha()
        player_sprite = graphics.Sprites(player_image)
        self.player = graphics.Player(player_sprite, x=400, y=300, frame_width=16, frame_height=16, scale=2)

        # --- Colliders (walls, map borders, etc.) ---
        self.physics.add_collider(physics.BoxCollider(200, 200, 300, 50))  # horizontal wall
        self.physics.add_collider(physics.BoxCollider(600, 500, 50, 200))  # vertical wall

        # --- Music ---
        self.track = "audio/bg_music/02_MysticForest.wav"
        self.audio_player.load_music(self.track)
        self.audio_player.play_music(-1)

    def handle_events(self, events):
        super().handle_events(events)

    def update(self, keys):
        # Update game logic
        self.player.update(keys)
        self.physics.handle_collisions(self.player)
        self.camera.update(self.player)

    def draw(self):
        # Clear + background
        self.surface.fill(self.background_color)

        # Zoom background
        zoom_rect = self.camera.apply(self.surface.get_rect())
        zoomed_bg = pygame.transform.scale(self.surface, (int(1600 * self.camera.zoom), int(1200 * self.camera.zoom)))
        self.screen.blit(zoomed_bg, zoom_rect)

        # Draw player
        player_rect = self.camera.apply(self.player.rect)
        scaled_image = pygame.transform.scale(
            self.player.image,
            (int(self.player.rect.width * self.camera.zoom), int(self.player.rect.height * self.camera.zoom))
        )
        self.screen.blit(scaled_image, player_rect)

        # Draw colliders (debug)
        for collider in self.physics.colliders:
            collider.draw(self.screen, camera=self.camera)

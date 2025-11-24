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

        # -- Tiles --
        tileset_image = pygame.image.load("graphics/tiles/flowerbush.png").convert_alpha()
        self.tiles = graphics.Tiles(tileset_image, physics_world=self.physics)
        self.flower_tile = self.tiles.create_tile(
            x=100, y=150, frame=0, width=16, height=16, scale=1, row=0
        )

        # --- Player setup ---
        player_image = pygame.image.load("graphics/sprites/male_chr01_sheet.png").convert_alpha()
        player_sprite = graphics.Sprites(player_image)
        self.player = graphics.Player(player_sprite, x=100, y=100, frame_width=16, frame_height=16, scale=2)

        # --- Colliders (walls, map borders, etc.) ---
        self.physics.add_collider(physics.BoxCollider(200, 200, 300, 50))  # horizontal wall
        self.physics.add_collider(physics.BoxCollider(600, 500, 50, 200))  # vertical wall

        # Testing - Set colliders visibility to true
        self.physics.set_debug(True)

        # Load tiles - flowers
        self.tileset_image = pygame.image.load("graphics/tiles/flowerbush.png").convert_alpha()

        self.flowers = graphics.Tiles(
            self.tileset_image,
            self.physics,
            has_physics=True,
            debug_collider=True
        )

        self.tiles = graphics.Tiles(
            self.tileset_image,
            self.physics,
            has_physics=True,
            debug_collider=True
        )

        # Disable physics entirely:
        # tiles.enable_physics(False)

        # --- Music ---
        self.track = "audio/bg_music/02_MysticForest.wav"
        self.audio_player.load_music(self.track)
        self.audio_player.play_music(-1)

    def handle_events(self, events):
        super().handle_events(events)

    def update(self, keys):
        # Pass the camera instance to player so it can control zoom
        self.player.update(keys, self.camera)

        # Handle collisions with walls
        self.physics.handle_collisions(self.player)

        # Update camera to follow player
        self.camera.update(self.player)

    def draw(self):
        # clear screen
        self.screen.fill((0, 0, 0))

        # next I apply the correct background color for the scene01 zone map - green
        self.screen.fill(self.background_color)

        # next I draw the tiles or the map
        self.flower_tile.draw(self.screen, self.camera)

        # then I handle drawing the player
        player_screen_rect = self.camera.apply(self.player.rect)
        self.screen.blit(self.player.image, player_screen_rect)

        # then the physics colliders if any
        for collider in self.physics.colliders:
            collider_rect = pygame.Rect(
                collider.x, collider.y, collider.width, collider.height
            )
            screen_rect = self.camera.apply(collider_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), screen_rect, 1)

        # lastly, I flip the display
        pygame.display.flip()

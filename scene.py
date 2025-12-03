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
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, keys, dt):
        pass

    def draw(self):
        pass


class Scene01(Scene):
    def __init__(self, screen):
        super().__init__(screen)

        # --- Core setup ---
        self.surface = pygame.Surface((1600, 1200))
        self.background_color = (100, 200, 100)

        # --- Systems ---
        self.physics = physics.Physics(1600, 1200)
        self.audio_player = audio.MusicPlayer()
        self.camera = camera.Camera(800, 600, zoom=2.0)

        # --- Tiles ---
        tileset_image = pygame.image.load("graphics/tiles/flowerbush.png").convert_alpha()
        self.tiles = graphics.Tiles(tileset_image, physics_world=self.physics)
        self.flower_tile = self.tiles.create_tile(
            x=100, y=150, frame=0, width=16, height=16, scale=1, row=0
        )

        # --- Player ---
        player_image = pygame.image.load("graphics/sprites/male_chr01_sheet.png").convert_alpha()
        player_sprite = graphics.Sprites(player_image)
        self.player = graphics.Player(player_sprite, x=100, y=100,
                                      frame_width=16, frame_height=16, scale=2)

        # --- Enemy NPC ---
        enemy01_image = pygame.image.load("graphics/sprites/enemy_01.png").convert_alpha()
        enemy01_sprite = graphics.Sprites(enemy01_image)
        self.enemy01 = graphics.NPC(enemy01_sprite, x=75, y=75,
                                    frame_width=16, frame_height=16, scale=2,
                                    chartype="enemy")

        # --- Physics Colliders ---
        self.physics.add_collider(physics.BoxCollider(200, 200, 300, 50))
        self.physics.add_collider(physics.BoxCollider(600, 500, 50, 200))
        self.physics.set_debug(True)

        # --- Music ---
        self.track = "audio/bg_music/02_MysticForest.wav"
        self.audio_player.load_music(self.track)
        self.audio_player.play_music(-1)

    def update(self, keys, dt):

        # Player update (no dt needed yet, but included)
        self.player.update(keys, self.camera, dt)

        # Enemy roaming update
        self.enemy01.update(True, dt)

        # Physics collision
        self.physics.handle_collisions(self.player)

        # Camera follows player
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(self.background_color)

        # Tiles
        self.flower_tile.draw(self.screen, self.camera)

        # Player
        player_screen_rect = self.camera.apply(self.player.rect)
        self.screen.blit(self.player.image, player_screen_rect)

        # Enemy
        enemy_screen_rect = self.camera.apply(self.enemy01.rect)
        self.screen.blit(self.enemy01.image, enemy_screen_rect)

        # Debug physics colliders
        for collider in self.physics.colliders:
            collider_rect = pygame.Rect(collider.x, collider.y,
                                        collider.width, collider.height)
            screen_rect = self.camera.apply(collider_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), screen_rect, 1)

        pygame.display.flip()

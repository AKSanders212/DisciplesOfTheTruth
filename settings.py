"""
Project: Disciples Of The Truth (Christian 2D RPG)
Author: Aaron Keith Sanders
Date: 19 October 2025
File: settings.py
"""
import pygame
import scene

pygame.init()

# Global single shared clock
clock = pygame.time.Clock()


class Engine:
    def __init__(self):
        self.title = None
        self.bg_color = None
        self.game_screen = None
        self.current_scene = None

    def Run(self, title, bg_color):
        """Main game loop."""
        self.title = title
        self.bg_color = bg_color
        self.game_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(self.title)

        # Load initial scene
        self.current_scene = scene.Scene01(self.game_screen)

        while self.current_scene.running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            # Compute REAL delta time (seconds)
            dt = clock.tick(60) / 1000.0

            # Event handling + updates
            self.current_scene.handle_events(events)
            self.current_scene.update(keys, dt)
            self.current_scene.draw()

        # Scene ended
        self.current_scene.audio_player.stop_music()
        pygame.quit()

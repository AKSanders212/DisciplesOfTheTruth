"""
Project: Disciples Of The Truth (Christian 2D RPG)
Author: Aaron Keith Sanders
Date: 19 October 2025
File: settings.py
"""
import pygame
import scene

# Global vars ------------------------------------------------------------------#
pygame.init()
clock = pygame.time.Clock()
# ------------------------------------------------------------------------------#


def TestGrid(background):
    background.fill((100, 200, 100))
    for x in range(0, 1600, 64):
        pygame.draw.line(background, (80, 180, 80), (x, 0), (x, 1200))
    for y in range(0, 1200, 64):
        pygame.draw.line(background, (80, 180, 80), (0, y), (1600, y))

    # Make sure to return the background, so it can be used
    return background


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

        clock = pygame.time.Clock()
        while self.current_scene.running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            # Event handling + updates
            self.current_scene.handle_events(events)
            self.current_scene.update(keys)
            self.current_scene.draw()

            pygame.display.flip()
            clock.tick(60)

        # Scene ended
        self.current_scene.audio_player.stop_music()
        pygame.quit()

"""
    Project: Disciples Of The Truth (Christian 2D RPG)
    Author: Aaron Keith Sanders
    Date: 19 October 2025
    File: settings.py
"""
import pygame

pygame.init()

class Engine:
    def __init__(self):
        self.title = None
        self.bg_color = None
        self.game_screen = None

    def Run(self, title, bg_color):
        """The Run() method controls the game engine logic and runs the game"""
        self.title = title
        self.bg_color = bg_color
        self.game_screen = pygame.display.set_mode((800, 600))

        # Game loop variable
        running = True

        # The game loop
        while running:

            # Pygame events
            for event in pygame.event.get():
                # Quit the event
                if event.type == pygame.QUIT:
                    running = False

            # Fill the screen with bg_color and flip the display to update it
            self.game_screen.fill(bg_color)
            pygame.display.flip()



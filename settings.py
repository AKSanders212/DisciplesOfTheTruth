"""
    Project: Disciples Of The Truth (Christian 2D RPG)
    Author: Aaron Keith Sanders
    Date: 19 October 2025
    File: settings.py
"""
import pygame
import graphics

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

        # Load a single 16x16 sprite from the spritesheet at (0, 0)
        sprite = graphics.Sprites()
        rect = pygame.Rect(0, 0, 16, 16)
        player = sprite.LoadSprite("graphics/sprites/male_chr01_sheet.png", rect)

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
            self.game_screen.blit(player, (50, 50))
            pygame.display.flip()

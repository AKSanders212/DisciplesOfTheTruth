"""
    Project: Disciples Of The Truth (Christian 2D RPG)
    Author: Aaron Keith Sanders
    Date: 19 October 2025
    File: settings.py
"""
import pygame
import graphics

pygame.init()
clock = pygame.time.Clock()

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
        player_image = pygame.image.load("graphics/sprites/male_chr01_sheet.png").convert_alpha()
        player_sprite = graphics.Sprites(player_image)
        player = graphics.Player(player_sprite, x=50, y=50, frame_width=16, frame_height=16, scale=2)

        # Game loop variable
        running = True

        # The game loop
        while running:

            # Pygame events
            for event in pygame.event.get():
                # Quit the event
                if event.type == pygame.QUIT:
                    running = False

            # Updates the players movement
            keys = pygame.key.get_pressed()
            player.update(keys)

            # Fill the screen with bg_color and flip the display to update it
            self.game_screen.fill(bg_color)
            self.game_screen.blit(player.image, player.rect)
            pygame.display.flip()

            clock.tick(60) # FPS

        pygame.quit()

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


class Camera:
    def __init__(self, width, height, zoom=1.0):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.zoom = zoom

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
        pygame.display.set_caption(self.title)

        # Load player
        player_image = pygame.image.load("graphics/sprites/male_chr01_sheet.png").convert_alpha()
        player_sprite = graphics.Sprites(player_image)
        player = graphics.Player(player_sprite, x=400, y=300, frame_width=16, frame_height=16, scale=2)

        # Create camera
        player_camera = Camera(800, 600, zoom=2.0)  # start zoomed in 2x

        # Test grid for movement - replace with a level scene background
        background = pygame.Surface((1600, 1200))
        background.fill((100, 200, 100))
        for x in range(0, 1600, 64):
            pygame.draw.line(background, (80, 180, 80), (x, 0), (x, 1200))
        for y in range(0, 1200, 64):
            pygame.draw.line(background, (80, 180, 80), (0, y), (1600, y))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            player.update(keys)

            # Zoom controls (Q/E)
            if keys[pygame.K_q]:
                player_camera.zoom = min(player_camera.zoom + 0.02, 4.0)
            if keys[pygame.K_e]:
                player_camera.zoom = max(player_camera.zoom - 0.02, 0.5)

            # Update camera position
            player_camera.update(player)

            # Draw world
            self.game_screen.fill(self.bg_color)

            # Draw background with zoom + camera offset
            bg_rect = player_camera.apply(background.get_rect())
            scaled_bg = pygame.transform.scale(background, (int(1600 * player_camera.zoom), int(1200 * player_camera.zoom)))
            self.game_screen.blit(scaled_bg, bg_rect)

            # Draw player (scale + offset)
            player_draw_rect = player_camera.apply(player.rect)
            scaled_image = pygame.transform.scale(
                player.image,
                (int(player.rect.width * player_camera.zoom), int(player.rect.height * player_camera.zoom))
            )
            self.game_screen.blit(scaled_image, player_draw_rect)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

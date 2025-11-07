"""
Project: Disciples Of The Truth (Christian 2D RPG)
Author: Aaron Keith Sanders
Date: 19 October 2025
File: settings.py
"""
import pygame
import graphics
import audio

pygame.init()
clock = pygame.time.Clock()


class SceneManager:
    def __init__(self, screen, surface, background, player, musicplayer, track, camera):
        self.screen = screen
        self.surface = surface
        self.background = background
        self.player = player
        self.musicplayer = musicplayer
        self.track = track
        self.camera = camera

    def load_scene(self, screen, surface, background, player,
                   camera):
        """Loads a new scene"""
        # clear the old background
        self.clear_background(screen)

        # load a new background
        surface.fill(background)

        # Update camera position
        camera.update(player)

        # Draw background with zoom + camera offset
        zoom_rect = camera.apply(surface.get_rect())
        zoomed_bg = pygame.transform.scale(surface,
                                           (int(1600 * camera.zoom), int(1200 * camera.zoom)))

        # Draws a new zoomed bg surface with a zoomed rect space
        screen.blit(zoomed_bg, zoom_rect)

        # Draw player (scale + offset)
        player_draw_rect = camera.apply(player.rect)
        scaled_image = pygame.transform.scale(
            player.image,
            (int(player.rect.width * camera.zoom), int(player.rect.height * camera.zoom))
        )

        # Draws to the screen the scaled background image with the camera applied to the player_rect
        screen.blit(scaled_image, player_draw_rect)

        return screen, surface

    def clear_background(self, screen):
        """Clears the previous screen from the previous scene"""
        screen.fill((0, 0, 0))  # fills the screen with black color

        return screen

    def scene_music(self):
        self.musicplayer.load_music(self.track)
        self.musicplayer.play_music(-1)


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

    def Run(self, title, bg_color):
        """The Run() method controls the game engine logic and runs the game"""
        self.title = title
        self.bg_color = bg_color
        self.game_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(self.title)

        # background
        background = (100, 200, 100)

        # Load player
        player_image = pygame.image.load("graphics/sprites/male_chr01_sheet.png").convert_alpha()
        player_sprite = graphics.Sprites(player_image)
        player = graphics.Player(player_sprite, x=400, y=300, frame_width=16, frame_height=16, scale=2)

        # Create camera
        player_camera = Camera(800, 600, zoom=2.0)  # start zoomed in 2x

        # Surface used for zoomed backgrounds
        surface = pygame.Surface((1600, 1200))

        # audio player for playing music
        audio_player = audio.MusicPlayer()

        # Music track (forest theme)
        track = "audio/bg_music/02_MysticForest.wav"

        # New scene manager
        scene01 = SceneManager(self.game_screen, surface, background, player, audio_player,
                               track, player_camera)

        # loads music for first scene
        scene01.scene_music()

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

            # Load the scene and its contents
            scene01.load_scene(self.game_screen, surface, background, player, player_camera)

            pygame.display.flip()
            clock.tick(60)

        if not running:
            audio_player.stop_music()
            audio_player.quit_music()

        pygame.quit()

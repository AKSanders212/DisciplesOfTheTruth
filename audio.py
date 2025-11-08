"""
Project: Disciples Of The Truth (Christian 2D RPG)
Author: Aaron Keith Sanders
Date: 8 November 2025
File: audio.py
"""
import pygame

pygame.init()


class MusicPlayer:
    """The MusicPlayer class is responsible for loading and playing music files"""
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None

    def load_music(self, path):
        """Responsible for loading music files"""
        # Load using a try catch block
        try:
            pygame.mixer.music.load(path)
            self.current_music = path
            print(f"Music file has been loaded: {path}")
        except pygame.error as e:
            print(f"An error occured loading the music file: {e}")

    def play_music(self, loops=-1):
        """Plays the loaded music -1 = infinite loop"""
        if self.current_music:
            pygame.mixer.music.play(loops) # play the music based on its loops
            print(f"Current music playing: {self.current_music}")
        else:
            print("No music has been loaded to play. Check your filetype and its path.")

    def stop_music(self):
        """Stops the current music playing"""
        pygame.mixer.music.stop()
        print("The music has stopped playing.")

    def pause_music(self):
        """Pauses the current playing music"""
        pygame.mixer.music.pause()
        print("The music has been paused.")

    def unpause_music(self):
        """Unpauses the current playing music"""
        pygame.mixer.music.unpause()
        print("The music has been unpaused.")

    def set_volume(self, volume):
        """Sets the volume from 0.0 to 1.0"""
        if 0.0 <= volume <= 1.0:
            pygame.mixer.music.set_volume(volume)
            print(f"Volume set to: {volume}")
        else:
            print("Is your volume set between 0.0 to 1.0?")

    def get_volume(self):
        """Returns the volume of the music"""
        return pygame.mixer.music.get_volume()

    def is_playing(self):
        """Determines if the current music is playing or not"""
        return pygame.mixer.music.get_busy()

    def quit_music(self):
        """Quits the playing music and cleans the file from memory"""
        pygame.mixer.quit()
        print("The music mixer has been turned off")






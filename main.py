"""
    Project: Disciples Of The Truth (Christian 2D RPG)
    Author: Aaron Keith Sanders
    Date: 19 October 2025
    File: main.py
"""
import pygame
import settings

# Initialize pygame
pygame.init()

# Globals
# Set the background color
bg_color = (0, 0, 0)
# Set the screen title
title = "Disciples of The Truth"


def main():
    # Create a new object for the Engine class in the settings file
    game = settings.Engine()
    game.Run(title, bg_color)


if __name__ == "__main__":
    main()

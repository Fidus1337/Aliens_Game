import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, game_window) -> None:
        super().__init__()

        self.screen = game_window.screen  # Reference to the game instance
        self.settings = game_window.settings  # Reference to the settings

        self.alien_speed = self.settings.alien_speed  # Set the speed of the alien

        # Load the image of the alien
        self.image = pygame.image.load('../images/alien.bmp')

        # Scale the image to be half its original size
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // 2,
                         self.image.get_height() // 2)
        )

        # Get the rect for the image
        self.rect = self.image.get_rect()

        # Place the alien at the top-left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's position as float for more precise movement
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the alien right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return True if the alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

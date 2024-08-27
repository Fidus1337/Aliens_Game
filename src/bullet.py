import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to make bullets fired from the ship"""

    def __init__(self, game_window) -> None:
        """Create bullet at the ships position"""

        super().__init__()
        self.screen = game_window.screen
        self.settings = game_window.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set ships position
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game_window.ship.rect.midtop

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        # Update the exact position of bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

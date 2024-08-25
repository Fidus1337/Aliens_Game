import pygame


class Ship:

    def __init__(self, game_window) -> None:
        "Initialize ship at start pos"
        self.screen = game_window.screen
        self.screen_rect = self.screen.get_rect()

        # Load the image and get its rect.
        self.image = pygame.image.load('../images/ship.bmp')
        self.rect = self.image.get_rect()

        # Each new ship should by at the center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at the current location"""
        self.screen.blit(self.image, self.rect)

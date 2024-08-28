import pygame


class Ship:
    """Definition for the ship class"""

    def __init__(self, game_window) -> None:
        """Initialize ship at start pos"""
        self.screen = game_window.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_window.settings

        # Load the image and get its rect.
        self.image = pygame.image.load('../images/ship.bmp')
        self.rect = self.image.get_rect()

        # Each new ship should be at the center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal and vertical position (ship's velocity).
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # For controllers of the ship
        self.moves_right = False
        self.moves_left = False
        self.moves_up = False
        self.moves_down = False

    def update_position(self):
        """Update the ship's position based on movement flags."""
        if self.moves_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moves_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        if self.moves_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moves_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at the current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)  # Update x temp var
        self.y = float(self.rect.y)  # Update y temp var

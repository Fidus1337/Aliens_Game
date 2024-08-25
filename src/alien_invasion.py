import sys

import pygame

from ship import Ship
from settings import Settings


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self) -> None:
        """Initialize the game, and create game resources"""
        pygame.init()

        # Initialize clock for normal rate
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Set windwo dimension
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # Set caption of the window
        pygame.display.set_caption("Alien invasion")

        # Set the background color.
        self.bg_color = self.settings.bg_color

        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            # Watch keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color)
            self.ship.blitme()

            # Make the most recently drawn screen visible
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    # # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

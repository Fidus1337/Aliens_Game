"""Here is all logic for alien_invasion game"""
# pylint: disable=no-member


# For quit function
import sys

# For all functions related to game-development
import pygame

# The ship, which will be added to the screen
from ship import Ship

# Settings of the game
from settings import Settings


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self) -> None:
        """Initialize the game, and create game resources"""
        pygame.init()

        # Initialize clock for normal rate
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Set windows dimension and make it fullscreen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)

        # Set caption of the window
        pygame.display.set_caption("Alien invasion")

        # Set the background color.
        self.bg_color = self.settings.bg_color

        # Init ship
        self.ship = Ship(self)

    def _check_keydown_events(self, event):
        """Checks keyup of the controllers and changes values"""
        if event.key == pygame.K_RIGHT:
            self.ship.moves_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moves_left = True
        elif event.key == pygame.K_UP:
            self.ship.moves_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moves_down = True

    def _check_keyup_events(self, event):
        """Checks keydown of the controllers and changes values"""
        if event.key == pygame.K_RIGHT:
            self.ship.moves_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moves_left = False
        elif event.key == pygame.K_UP:
            self.ship.moves_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moves_down = False

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    sys.exit()
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        """Filling with color screen, updating frames(limit 60 fps), show the ship"""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.bg_color)

        self.ship.blitme()

        # Make the most recently drawn screen visible
        pygame.display.flip()

        # Make 60 fps only
        self.clock.tick(60)

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            # Watch keyboard and mouse events
            self._check_events()
            self._update_screen()
            self.ship.update_position()


if __name__ == '__main__':
    # # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

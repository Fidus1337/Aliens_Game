"""Here is all logic for alien_invasion game"""
# pylint: disable=no-member

# Timer
from time import sleep

# For quit function
import sys

# For all functions related to game-development
import pygame

# The ship, which will be added to the screen
from ship import Ship

# Settings of the game
from settings import Settings

# Bullets
from bullet import Bullet

# Alien
from alien import Alien

# Game statistics
from game_stats import GameStats


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self) -> None:
        """Initialize the game, and create game resources"""
        pygame.init()

        # Initialize clock for normal rate
        self.clock = pygame.time.Clock()

        # Settings of the game
        self.settings = Settings()
        self.game_active = True

        # Initialize bullets group
        self.bullets = pygame.sprite.Group()

        # Set windows dimension and make it fullscreen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE)

        # Set caption of the window
        pygame.display.set_caption("Alien invasion")

        # Set the background color.
        self.bg_color = self.settings.bg_color

        # Init ship
        self.ship = Ship(self)

        # Init game statistics
        self.game_stistics = GameStats(self)

        # Create an array, which will be filled with aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def _check_fleet_edges(self):
        """Check if any aliens reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and calculate the number of aliens in a row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - 1.5 * alien_width
        number_aliens_x = int(available_space_x // (1.5 * alien_width))

        available_space_y = self.settings.screen_height - 3 * alien_height
        number_rows = int(available_space_y // (2 * alien_height))

        # Create the fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                x_position = alien_width + 1.5 * alien_width * alien_number
                self._create_alien(x_position, alien_height +
                                   2 * alien_height * row_number)

    def _create_alien(self, x_position, y_position):
        """Create and add new alien to array"""
        # Create alien class instance
        alien = Alien(self)

        # Set position x and y
        alien.x = x_position
        alien.rect.x = x_position
        alien.rect.y = y_position

        # Adding alien to fleet
        self.aliens.add(alien)

    def _check_keydown_events(self, event):
        """Checks keydown of the controllers and changes values"""
        if event.key == pygame.K_RIGHT:
            self.ship.moves_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moves_left = True
        elif event.key == pygame.K_UP:
            self.ship.moves_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moves_down = True

    def fire_bullet(self):
        """Add new bullet to the bullets array, which will update each frame"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        """Checks keyup of the controllers and changes values"""
        if event.key == pygame.K_RIGHT:
            self.ship.moves_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moves_left = False
        elif event.key == pygame.K_UP:
            self.ship.moves_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moves_down = False
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

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

    def _update_bullets(self):
        """Update position of the bullets and get rid of the old bullets"""
        # Update position of the bullets
        self.bullets.update()

        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        # Get rid of the old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Try to launch new fleet instead of the old
        self._try_launch_new_fleet()

    def _check_if_ship_collides_with_aliens(self):
        """Look for alien-ship collisions."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_takes_damage_respond()  # The ship takes damage

    def _ship_takes_damage_respond(self):
        """Ship loses one life and the game clears from bullets and aliens"""
        # Subtract one life
        self.game_stistics.ships_left -= 1

        if self.game_stistics.ships_left > 0:
            # Destroy all aliens and bullets
            self.bullets.empty()
            self.aliens.empty()

            # Create new fleet and place ship at the center
            self._create_fleet()
            self.ship.center_ship()

            # Reset ship movement flags
            self.ship.moves_right = False
            self.ship.moves_left = False
            self.ship.moves_up = False
            self.ship.moves_down = False

            # Pause game
            sleep(0.5)
        else:
            # Stop the game
            self.game_active = False

    def _try_launch_new_fleet(self):
        """Launch new fleet if the old one has been destroyed"""
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _update_screen(self):
        """Filling with color screen, updating frames(limit 60 fps), show the ship"""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.bg_color)

        self.ship.blitme()

        self.aliens.draw(self.screen)

        # Draw all bullets on the screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        # Check if the controlled ship has collided with an alien
        self._check_if_ship_collides_with_aliens()

        # Check if aliens have touched the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_takes_damage_respond()
                break

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            # Watch keyboard and mouse events
            self._check_events()

            if self.game_active:
                # Update bullets' position and delete bullets that are off the screen
                self._update_bullets()
                # Update aliens' position
                self._update_aliens()
                # Update ship's position
                self.ship.update_position()

            # Update screen
            self._update_screen()

            # Make 60 fps only
            self.clock.tick(60)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

"""General settings"""


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self) -> None:
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 3
        self.ship_lifes = 3

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 300
        self.bullet_height = 50
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        # The setting fleet_drop_speed controls how quickly the fleet drops down the screen each time an alien reaches either edge.
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

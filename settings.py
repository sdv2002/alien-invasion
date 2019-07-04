"""module with class Settings"""


class Settings:
    """Class to store all the game settings."""
    def __init__(self):
        """Initialisere static game settings."""
        # Screen parameters
        self.screen_width = 700
        self.screen_height = 500
        self.bg_color = (0, 0, 0)
        
        # Color star
        self.star_color = (255, 255, 255)
        
        # Ship settings
        self.ship_limit = 3
        
        # Bullet parameters
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 3
        
        # Alien settings
        self.fleet_drop_speed = 10
        
        # Game acceleration rate
        self.speedup_scale = 1.1
        # Alien value growth rate
        self.score_scale = 1.1
        self.ship_speed_factor = None
        self.bullet_speed_factor = None
        self.alien_speed_factor = None
        self.fleet_direction = None
        self.alien_points = None
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initializes settings that change during the game."""
        self.ship_speed_factor = 0.4
        self.bullet_speed_factor = 0.6
        self.alien_speed_factor = 0.3
        # fleet_direction = 1 denotes movement to the right; -1 - left.
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50
        
    def increase_speed(self):
        """Increases speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

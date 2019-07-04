"""module with class Bullet"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class to control bullets fired by the ship."""
    
    def __init__(self, ai_settings, screen, ship):
        """Creates a bullet object at the current ship position."""
        super(Bullet, self).__init__()
        self.screen = screen
        # Creating a bullet in position (0,0) and assigning the correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # The position of the bullet is stored in float.
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        """Moves the bullet up the screen."""
        self.y -= self.speed_factor
        # Update rectangle position.
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Bullet output on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

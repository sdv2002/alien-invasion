"""module with class Ship"""

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class representing a ship."""
    
    def __init__(self, ai_settings: object, screen: object) -> object:
        """Initializes the ship and sets its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Uploading a ship image and getting a rectangle.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Each new ship appears at the bottom of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Save the real coordinate of the center of the ship.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Move flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
        """Updates the position of the ship with the flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
            
        # Update rect attribute based on self.center.
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        
    def blitme(self):
        """Draws the ship in the current position."""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Places the ship in the center of the bottom side."""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom - self.rect.height / 2

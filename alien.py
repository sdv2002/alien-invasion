"""module with class Alien"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class that represents one alien."""
    
    def __init__(self, ai_settings, screen):
        """Initializes an alien and sets its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Loading the alien image and assigning the rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # Each new alien appears in the upper left corner of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Preserving the exact position of the alien.
        self.x = float(self.rect.x)
    
    def blitme(self):
        """Displays the alien in the current position."""
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """Moves the alien left or right."""
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
    def check_edges(self):
        """Returns True if the alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    

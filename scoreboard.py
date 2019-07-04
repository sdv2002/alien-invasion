"""module with class Scoreboard"""

import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """Class to output game information."""
    
    def __init__(self, ai_settings, screen, stats):
        """Initialisere attributes scoring."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # Font settings to display the account.
        self.text_color = (250, 250, 250)
        self.font = pygame.font.SysFont(None, 38)
        # The rendering of accounts.
        self.prep_high_score()
        self.prep_score()
        self.prep_level()
        self.prep_ships()
        
    def prep_score(self):
        """Converts the score into a graphic image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                    self.text_color, self.ai_settings.bg_color)
        # The output of the account at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10
        
    def prep_high_score(self):
        """Converts a record score in a graphic image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                self.text_color, self.ai_settings.bg_color)
        # The record is centered on the top side.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top
        
    def show_score(self):
        """Displays the score on screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Вывод кораблей.
        self.ships.draw(self.screen)
        
    def prep_level(self):
        """Converts a level in graphical image."""
        self.level_image = self.font.render(str(self.stats.level), True,
                                self.text_color, self.ai_settings.bg_color)
        # The level is displayed under current account.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        
    def prep_ships(self):
        """Reports the number of remaining ships."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

"""module with class GameStats"""

import json

class GameStats():
    """Stat tracking for the game"""
    
    def __init__(self, ai_settings):
        """Initialisere statistics."""
        self.ai_settings = ai_settings
        # Read record from file
        filename = 'images\high_score.json'
        try:
            with open(filename,  'r') as file_object:
                content = json.load(file_object)
        except FileNotFoundError:
            content = 0
        self.high_score = content
        # The game starts in an inactive state.
        self.game_active = False
        self.reset_stats()
        
    
    def reset_stats(self):
        """Initialisere statistics, changing the course of the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        

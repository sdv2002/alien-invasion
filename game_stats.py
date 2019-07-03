import json

class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""
    
    def __init__(self, ai_settings):
        """Инициализирует статистику."""
        self.ai_settings = ai_settings
        # Считывание рекорда из файла
        filename = 'images\high_score.json'
        try:
            with open(filename,  'r') as file_object:
                content = json.load(file_object)
        except FileNotFoundError:
            content = 0
        self.high_score = content
        # Игра Alien Invasion запускается в неактивном состоянии.
        self.game_active = False
        self.reset_stats()
        
    
    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        

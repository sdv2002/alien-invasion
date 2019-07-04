"""module with class Button"""

import pygame.font

class Button():
    
    def __init__(self, ai_settings, screen, msg):
        """Initializes the attributes of the button."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Assign sizes and properties of buttons.
        self.width, self.height = 200, 50
        self.button_color = (50, 220, 118)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # Constructing a rect object and aligning it to the center of the screen.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # Button message
        self.prep_msg(msg)
        
    def prep_msg(self, msg):
        """Converts msg to a rectangle and aligns the text to the center."""
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        # Display a blank button and display a message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

"""This is the main module in the game"""

import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


def run_game():
    """Initializes the game and creates a screen object."""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Create a play button.
    play_button = Button(ai_settings, screen, "Play")
    # Create instances of GameStats and Scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Creating a ship, a group of bullets and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    # Creating a starry sky
    stars = gf.create_starry_sky(ai_settings, screen)
    # Creating a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Run the main loop.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb,
                              ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen,
                             ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship,
                         aliens, bullets, stars, play_button)


run_game()

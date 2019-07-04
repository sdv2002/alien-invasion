"""module with game functions"""

import sys
import json
from time import sleep
import pygame
import random
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, stats, screen,
                         ship, bullets):
    """Reacts to keystrokes."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE or event.key == 306:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        exit_with_saving(stats)
    elif event.key == pygame.K_p:
        stats.game_active = not stats.game_active
        stats.pause = not stats.pause


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fires a bullet if the maximum has not yet been reached."""
    # Creating a new bullet and including it in the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        # gunfire
        pygame.mixer.Sound(r'images\laser.wav').play()


def check_keyup_events(event, ship):
    """Reacts to the release of keys."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button,
                 ship, aliens, bullets):
    """Tracking keyboard and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_with_saving(stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats,
                                 screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Launches a new game when you click the Play button."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings.
        ai_settings.initialize_dynamic_settings()
        # The mouse pointer is hiding.
        pygame.mouse.set_visible(False)
        # Reset game statistics.
        stats.reset_stats()
        stats.game_active = True
        # Reset images of accounts and level.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Cleaning lists of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Creating a new fleet and placing the ship in the center.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens,
                  bullets, stars, play_button):
    """Updates the image on the screen and displays a new screen."""
    screen.fill(ai_settings.bg_color)
    # We draw the star sky
    for x, y in stars.items():
        pygame.draw.circle(screen, ai_settings.star_color, (x, y), 0)
    # All bullets are displayed behind images of the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Invoice withdrawal.
    sb.show_score()
    # The Play button is displayed if the game is inactive.
    if not stats.game_active and not stats.pause:
        play_button.draw_button()
    # Displays the last drawn screen.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Updates bullet positions and destroys old bullets."""
    # Update bullet positions.
    bullets.update()
    # Remove bullets that go beyond the edge of the screen.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Check for hits in the aliens.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    """Handling collisions of bullets with aliens."""
    # Removing bullets and aliens involved in collisions.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # explosion
        pygame.mixer.Sound('images\\bum.wav').play()
        # Scoring
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:
        # Destruction of bullets, increasing speed and creating a new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        # Level increase.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Calculates the number of aliens in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determines the number of rows that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Creates an alien and places it in a row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 50 + alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creates a fleet of aliens."""
    # Creating an alien and calculating the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # Creating a fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def create_starry_sky(ai_settings):
    """Creates a dictionary with random dots for the starry sky."""
    stars = {}
    for i in range(800):
        a = random.randint(0, ai_settings.screen_width)
        b = random.randint(0, ai_settings.screen_height)
        stars[a] = b
    return stars


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Handles the collision of a ship with a alien."""
    if stats.ships_left > 1:
        # Reducing ships_left.
        stats.ships_left -= 1
        # Update game information.
        sb.prep_ships()
        # Clear lists of the aliens and bullets.
        aliens.empty()
        bullets.empty()
        # The creation of a new fleet and vehicle placement in the center.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Checks if the aliens get to the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # The same happens in the collision with the ship.
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """
    Checks whether or not the fleet edge of the screen,
    then updates the positions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Check conflicts "alien ship".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    # Check the aliens reach the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Reacts to the approach of the alien to the edge of the screen."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Down the entire fleet and change the direction of the fleet."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_high_score(stats, sb):
    """Checks to see if a new record."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def exit_with_saving(stats):
    """Writes a record points to the file and closes the program"""
    filename = r'images\high_score.json'
    with open(filename, 'w') as file_object:
        json.dump(stats.high_score, file_object)
    sys.exit()

import sys
import json
from time import sleep
import pygame
import random
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


def check_keydown_events(event, ai_settings, stats, screen,
                         ship, aliens, bullets):
    """Реагирует на нажатие клавиш."""
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
    # elif event.key == pygame.K_p and not stats.game_active:
    #     start_game(ai_settings, screen, stats, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут."""
    # Создание новой пули и включение ее в группу bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        # Звук выстрела
        pygame.mixer.Sound('images\laser.wav').play()


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
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
    """Отслеживание событий клавиатуры и мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_with_saving(stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats,
                                 screen, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек.
        ai_settings.initialize_dynamic_settings()
        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)
        # Сброс игровой статистики.
        stats.reset_stats()
        stats.game_active = True
        # Сброс изображений счетов и уровня.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens,
                  bullets, stars, play_button):
    """Обновляет изображения на экране и отображает новый экран."""
    screen.fill(ai_settings.bg_color)
    # Рисуем звездное небо
    for x, y in stars.items():
        pygame.draw.circle(screen, ai_settings.star_color, (x, y), 0)
    # Все пули выводятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Вывод счета.
    sb.show_score()
    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()
    # Отображение последнего прорисованного экрана.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиций пуль.
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Проверка попаданий в пришельцев.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    """Обработка коллизий пуль с пришельцами."""
    # Удаление пуль и пришельцев, участвующих в коллизиях.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # Звук зрыва
        pygame.mixer.Sound('images\\bum.wav').play()
        # Начисление очков
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:
        # Уничтожение пуль, повышение скорости и создание нового флота.
        bullets.empty()
        ai_settings.increase_speed()
        # Увеличение уровня.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 50 + alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # Создание флота пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def create_starry_sky(ai_settings, screen):
    """Создает словарь со случайными точками для звездного неба"""
    stars = {}
    for i in range(800):
        WHITE = (255, 255, 255)
        a = random.randint(0, ai_settings.screen_width)
        b = random.randint(0, ai_settings.screen_height)
        stars[a] = b
    return stars


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.ships_left > 1:
        # Уменьшение ships_left.
        stats.ships_left -= 1
        # Обновление игровой информации.
        sb.prep_ships()
        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Пауза.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка коллизий "пришелец-корабль".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    # Проверка пришельцев, добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def exit_with_saving(stats):
    """Записывает рекордные очки в файл и закрывает программу"""
    filename = 'images\high_score.json'
    with open(filename, 'w') as file_object:
        json.dump(stats.high_score, file_object)
    sys.exit()

import sys
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #Создание новой пули и включение ее в группу Bullets
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit(0)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов появляющихся на экране"""
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    

def check_events(ai_settings, screen, ship, bullets):
    #Отслеживание событий клавиатуры и мыши.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #try:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            #except:
           #     print('Error in exit')
            #    return

def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Обновляет изображение на экране и отображает новый экран."""
    #При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)
    #Все пули выводятся позади корабля и прищельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #Отображение последнего прорисованного экрана
    pygame.display.flip()

def update_bullets(bullets):
    """Обновляет позиции пуль и уничтожает старые пули"""
    #Обновление позиций пуль
    bullets.update()

    #Удаление пуль, вышедших за границу экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    #Создание пришельца и вычисление количества пришельцев в ряду
    #Интервал между соседними пришельцами равен одной ширине пришельца

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    #print(number_rows)
    #Создание первого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
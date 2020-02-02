import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

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
    

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            #except:
           #     print('Error in exit')
            #    return
def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнокпи Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Сброс игровых настроек
        ai_settings.initialize_dynamic_settings()

        #Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

        #Сброс игровой статистики
        stats.reset_stats()
        stats.game_active = True
        
        #Очистка списка пришельцев и пуль
        aliens.empty()
        bullets.empty()

        #Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображение на экране и отображает новый экран."""
    #При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)
    #Все пули выводятся позади корабля и прищельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #Вывод счета
    sb.show_score()
    
    #Кнопка Play отображается в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()
    #Отображение последнего прорисованного экрана
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули"""
    #Обновление позиций пуль
    bullets.update()

    #Удаление пуль, вышедших за границу экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))
    #Проверка попаданий в прешельцев.
    #При обнаружении попадания удалить пулю и пришельца
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Обработка коллизий пуль с пришельцами"""
    #Удаление пуль и пришельцев, участвующих в коллизиях
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        #Уничтожение существующих пуль, повышение скорости и создание нового флота
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

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

def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцами края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет достиг ли флот края экрана,
    после чего Обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #Проверка коллизий пришелец-корабль
    if pygame.sprite.spritecollide(ship, aliens, False):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    #Проверка пришельцев добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.ship_left > 0:
        #Уменьщение ships_left
        stats.ship_left -= 1
        
        #Очистка списка пришельцев и пуль
        aliens.empty()
        bullets.empty()
        
        #Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

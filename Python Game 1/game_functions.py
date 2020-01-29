import sys
import pygame
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #Создание новой пули и включение ее в группу Bullets
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


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

def update_screen(ai_settings, screen, ship, bullets):
    """Обновляет изображение на экране и отображает новый экран."""
    #При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)
    #Все пули выводятся позади корабля и прищельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    #Отображение последнего прорисованного экрана
    pygame.display.flip()
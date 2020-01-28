import sys
import pygame

def check_events(ship):
    #Отслеживание событий клавиатуры и мыши.
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
            pygame.quit()
            #try:
            sys.exit(0)
       elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True

       elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            if event.key == pygame.K_LEFT:
                ship.moving_left = False
            #except:
           #     print('Error in exit')
            #    return

def update_screen(ai_settings, screen, ship):
    """Обновляет изображение на экране и отображает новый экран."""
    #При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    #Отображение последнего прорисованного экрана
    pygame.display.flip()
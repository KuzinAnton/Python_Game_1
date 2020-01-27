import sys
import pygame

def check_events():
    #Отслеживание событий клавиатуры и мыши.
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
            pygame.quit()
            #try:
            sys.exit(0)
            exit
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
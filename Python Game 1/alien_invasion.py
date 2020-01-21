import sys
import pygame

def run_game():
    #Инициализирует игру и создает объект экрана
    pygame.init()
    screen = pygame.display.set_mode((1200,800))
    pygame.display.set_caption('Alien Invasion')
    #Назначение цвета фона
    bg_color = (230, 230, 230)

    #Запуск основного цикла игры
    while True:
        #Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                except:
                    print('Error in exit')
                    return
        #При каждом проходе цикла перерисовывается экран
        screen.fill(bg_color)
        #Отображение последнего прорисованного экрана
        pygame.display.flip()

run_game()
import pygame
from settings import Settings
from ship import Ship


import game_functions as gf

def run_game():
    #Инициализирует игру и создает объект экрана
    
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    #Создание корабля
    ship = Ship(screen,ai_settings)
    #Создание группы для хранения пуль
    bullets = pygame.sprite.Group()
    
    #Запуск основного цикла игры
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, ship, bullets)

run_game()
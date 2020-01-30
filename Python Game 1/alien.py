import pygame

class Alien(pygame.sprite.Sprite):
    """Класс представляющий одного прешельца"""
    def __init__(self, ai_settings, screen):
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Загрузка изображений пришельца и назначение атрибута rect.
        self.image = pygame.image.load('Python Game 1/images/alien.bmp')
        self.rect = self.image.get_rect()

        #Каждый новый прешелец появляется в левом верхнем углу экрана.
        self.rect.y = self.rect.width
        self.rect.x = self.rect.height

        #Сохранение точной позиции пришельца.
        self.x = float(self.rect.x)

    def blitme(self):
        """Выводит пришельца в текущем положении"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Возвращает True если пришелец находиться у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        """Перемещает пришельца вправо"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

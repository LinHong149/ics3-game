import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

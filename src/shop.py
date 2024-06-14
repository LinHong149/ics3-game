from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

class Shop:
    def __init__(self, screen):
        self.screen = screen
        pass

    def draw(self):
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Shop', True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))

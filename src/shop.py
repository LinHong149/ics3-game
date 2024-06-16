from settings import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK
import pygame

class Shop:
    def __init__(self, screen):
        self.screen = screen
        pass

    def draw(self):
        font = pygame.font.SysFont('arial', 40)

        # Draws black opaque background
        background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)) 
        background.fill((0,0,0))
        background.set_alpha(120)
        self.screen.blit(background, (0, 0))

        # Draws shop title
        title = font.render('Shop', True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))


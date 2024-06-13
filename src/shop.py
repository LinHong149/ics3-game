from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

class Shop:
    def __init__(self, screen):
        self.screen = screen
        pass

    def draw(self):
        font = pygame.font.SysFont('arial', 40)
        title = font.render('My Game', True, (255, 255, 255))
        start_button = font.render('Start', True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))
        self.screen.blit(start_button, (SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_HEIGHT/2 + start_button.get_height()/2))


    # def __init__(self, game):
    #     self.game = game
    #     self.shop_prices = {
    #         'seed': 10,
    #         'dirt': 5,
    #         'tool': 20
    #     }
    #     self.crop_prices = {
    #         'potato': 10,
    #         'carrot': 8,
    #     }

    # def buy_item(self, item):
    #     if item in self.shop_prices:
    #         cost = self.shop_prices[item]
    #         if self.game.currency.subtract(cost):
    #             # Add to inventory
    #             return True
    #     return False

    # def sell_crop(self, crop):
    #     price = self.crop_prices[crop]
    #     self.game.currency.add(price)
    #     # Remove from inventory
    #     return True

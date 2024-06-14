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

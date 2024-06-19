from settings import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, WHITE
import pygame

class Shop:
    click_buffer = 0
    def __init__(self, screen, currency, items_prices, font):
        self.screen = screen
        self.currency = currency
        self.items_prices = items_prices
        self.font = font
        self.sell_button_rect = pygame.Rect(SCREEN_WIDTH-300-300, 400, 300, 60)

    def draw(self, inventory):
        font = pygame.font.SysFont('arial', 40)

        # Draws black opaque background
        background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)) 
        background.fill((0,0,0))
        background.set_alpha(120)
        self.screen.blit(background, (0, 0))

        # Draws shop title
        title = font.render('Shop', True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2 - 200))

        buy_header = font.render('Buy', True, WHITE)
        self.screen.blit(buy_header, (SCREEN_WIDTH/2 - buy_header.get_width()/2 - 200, SCREEN_HEIGHT/2 - title.get_height()/2 - 50))

        sell_header = font.render('Sell', True, WHITE)
        self.screen.blit(sell_header, (SCREEN_WIDTH/2 - sell_header.get_width()/2 + 190, SCREEN_HEIGHT/2 - title.get_height()/2 - 50))

        # Draw shop buttons
        buy_dirt_button = pygame.Rect(300,400, 300, 60)
        buy_carrot_seed_button = pygame.Rect(300,500, 300, 60)
        pygame.draw.rect(self.screen, WHITE, buy_dirt_button, 2)
        pygame.draw.rect(self.screen, WHITE, buy_carrot_seed_button, 2)

        buy_dirt_text = self.font.render("Buy Dirt $20", True, WHITE)
        buy_seeds_text = self.font.render("Buy Seeds $8", True, WHITE)
        self.screen.blit(buy_dirt_text, (buy_dirt_button.x + 10, buy_dirt_button.y + 10))
        self.screen.blit(buy_seeds_text, (buy_carrot_seed_button.x + 10, buy_carrot_seed_button.y + 10))
        
        if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - self.click_buffer > 200:
                self.click_buffer = pygame.time.get_ticks()
                mouse_pose = pygame.mouse.get_pos()

                if buy_dirt_button.collidepoint(mouse_pose):
                    self.currency.buy(self.items_prices["dirt"], "dirt")

                elif buy_carrot_seed_button.collidepoint(mouse_pose):
                    self.currency.buy(self.items_prices["carrot_seeds"], "carrot_seeds")

        # Button for selling crops
        pygame.draw.rect(self.screen, WHITE, self.sell_button_rect, 2)
        if inventory.get_items().get("carrot", 0) > 0:
            sell_text = self.font.render("Sell Carrot $12", True, WHITE)
            self.screen.blit(sell_text, (self.sell_button_rect.x + 10, self.sell_button_rect.y + 10))
        else:
            sell_text = self.font.render("No Carrots", True, WHITE)
            self.screen.blit(sell_text, (self.sell_button_rect.x + 10, self.sell_button_rect.y + 10))


    def handle_event(self, event, inventory):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.sell_button_rect.collidepoint(event.pos):
                if inventory.get_items().get("carrot", 0) > 0:
                    self.sell_crop(inventory)

    def sell_crop(self, inventory):
        if inventory.get_items().get("carrot", 0) > 0:
            inventory.remove_item("carrot", 1)
            self.currency.add(self.items_prices["carrot"])



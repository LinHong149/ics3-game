import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, GREEN, BLUE, RED, YELLOW
from currency import Currency

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        # Set initial currency to 100
        self.day = 1
        self.currency = Currency(amount=100)
        self.font = pygame.font.Font(None, 36)  # Default font and size
        self.setup()

    def setup(self):
        # Initialize game components (e.g., player, farm, shop)
        pass
    
    def handle_event(self, event):
        # Handle input events
        pass
    
    def update(self):
        # Update game state
        pass
    
    def draw(self):
        # Draw game elements
        pass

    def draw_text(self):
        # currency_text = str(self.currency.get_amount())
        currency_text = str(self.currency.get_amount())
        text_surface = self.font.render(currency_text, True, WHITE)
        text_box = text_surface.get_rect()
        text_box.bottomright = (SCREEN_WIDTH, 32)
        self.screen.blit(text_surface, text_box)  # Draw at the top-left corner
        
    def next_day(self):
        self.day += 1
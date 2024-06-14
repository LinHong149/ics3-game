import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, GREEN, BLUE, RED, YELLOW
from currency import Currency

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        # Set initial currency to 100
        self.day = 1
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

    def next_day(self):
        self.day += 1
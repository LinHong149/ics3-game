# Import libraries
import pygame
from pytmx.util_pygame import load_pygame
import csv
import json
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, GREEN, BLUE, RED, YELLOW
from game import Game
from playerSprite import PlayerSprite
from map import Map
from camera import Camera
from shop import Shop
from inventory import Inventory
from currency import Currency
from toolbar import Toolbar


# Variables
PLAYER_ACTION_SPRITE_DIMENTION = 48
PLAYER_MOVEMENT_SPRITE_DIMENTION= 32
DIMENTION = 32
PLAYER_SPRITE_MOVEMENT_ROW_LIST = ["standing_front", "standing_side", "standing_back", "walking_front", "walking_side", "walking_back"]
PLAYER_SPRITE_ACTION_ROW_LIST = ["axe_side", "axe_front", "axe_back", "hoe_side", "hoe_front", "hoe_back", "watering_front", "watering_back", "watering_side"]
PLAYER_SPRITE_MOVEMENT_ROW = 0
PLAYER_SPRITE_MOVEMENT_COL = 0
PLAYER_X = 1425
PLAYER_Y = 830
MOVEMENT_SPEED = 2
SCALE = 2.5
FLIP_CHARACTER = True
OPEN_SHOP = False
SHOP_POSE = (35, 18)
TILE_X = 0
TILE_Y = 0
INITIAL_CURRENCY = 100
DIRECTION = "u"
PLAYER_SPRITE_SHEET = None
PLAYER = None
font = None
screen = None
game_map = None
toolbar = None
clock = None
inventory = None
sound = None
running = True
sound_effect_playing = False
click_buffer = 0
alpha = 0
black_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
black_bg.fill(BLACK)


def init_pygame():
    # Initialize display
    global screen, clock, running, font, PLAYER_MOVEMENT_SPRITE, PLAYER_ACTION_SPRITE, PLAYER_WATER_SPRITE, SHEETS_LIST, sound
    pygame.init()
    pygame.display.set_caption('Title')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont('arial', 40)

    # Initialize Music
    pygame.mixer.init()
    # background_sound = pygame.mixer.Sound("../assets/sounds/background.mp3")
    # background_sound.play()
    # background_sound.set_volume(0.4)

    sound = pygame.mixer.Sound("../assets/sounds/effects/grass.mp3.ogg")

    PLAYER_MOVEMENT_SPRITE = pygame.image.load('../assets/images/player/Player.png').convert_alpha()
    PLAYER_HOE_SPRITE = pygame.image.load("../assets/images/player/Player_Hoe.png").convert_alpha()
    PLAYER_WATER_SPRITE = pygame.image.load("../assets/images/player/Player_Water.png").convert_alpha()
    SHEETS_LIST = [PLAYER_MOVEMENT_SPRITE, PLAYER_HOE_SPRITE, PLAYER_WATER_SPRITE]

def fade_in():
    global black_bg
    for alpha in range(0, 256, 5):
        black_bg.set_alpha(alpha)
        screen.blit(black_bg, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

def fade_out(text_surfaces, text_rects):
    global black_bg
    for alpha in range(255, -1, -5):
        black_bg.set_alpha(alpha)
        screen.fill(BLACK)  # Ensure the screen is filled with black
        for text_surface, text_rect in zip(text_surfaces, text_rects):
            screen.blit(text_surface, text_rect)  # Draw the text again to keep it visible during fade-out
        screen.blit(black_bg, (0, 0))  # Apply the fading effect
        pygame.display.flip()
        clock.tick(FPS)

def prologue():
    global alpha, running, black_bg

    texts = [
        "In the beginning, there was nothing but a vast, endless sea.",
        "A god, feeling curious, created a small island.",
        "On the island, they placed a human with a special task.",
        "The human must farm crops, earn dirt, and expand the land.",
        "With each expansion, the human would transform the ocean into a thriving paradise."
    ]

    for text in texts:
        screen.fill(BLACK)
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if font.size(current_line + word)[0] < SCREEN_WIDTH - 200:  # Adjust 200 for padding
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)  # Append the last line

        text_surfaces = [font.render(line, True, WHITE) for line in lines]
        text_rects = [text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + (i * font.size(lines[0])[1]))) for i, text_surface in enumerate(text_surfaces)]
        
        fade_out(text_surfaces, text_rects)
        
        for text_surface, text_rect in zip(text_surfaces, text_rects):
            screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 3000:  # Display text for 4 seconds
            black_bg.set_alpha(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return
            screen.fill(BLACK)
            for text_surface, text_rect in zip(text_surfaces, text_rects):
                screen.blit(text_surface, text_rect)
            pygame.display.flip()

        fade_in()


def sound_effect(file, play):
    global sound
    sound = pygame.mixer.Sound(file)
    if play:
        sound.play(1)
        return True
    elif not play:
        sound.stop()
        return False

def draw_next_day_button(screen):
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 100
    next_day_button = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 10 , SCREEN_HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BLACK, next_day_button)
    return next_day_button

def draw_toolbar(screen, toolbar, font):
    screen_width = screen.get_width()
    item_width = 100  # Width of each toolbar item
    item_height = 40  # Height of the toolbar
    x = (screen_width - (item_width * len(toolbar.items))) // 2  # Center the toolbar

    for index, item in enumerate(toolbar.items):
        rect = pygame.Rect(x + index * item_width, screen.get_height() - item_height - 10, item_width, item_height)
        color = (255, 0, 0) if index == toolbar.selected_index else (255, 255, 255)
        pygame.draw.rect(screen, color, rect, 2)  # Draw the border
        text_surface = font.render(item, True, color)
        screen.blit(text_surface, (rect.x + 10, rect.y + 10))  # Center text within the item

def draw_inventory(screen, inventory, font):
    x, y = 10, 10
    for item, quantity in inventory.get_items().items():
        item_text = f"{item}: {quantity}"
        text_surface = font.render(item_text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))
        y += 30  # Move down for the next item

def draw_currency(screen, currency, font):
    global SCREEN_WIDTH
    currency_text = f"Currency: {currency.get_amount()}"
    text_surface = font.render(currency_text, True, (255, 255, 255))
    text_width = text_surface.get_width()
    screen.blit(text_surface, (SCREEN_WIDTH - text_width - 10, 10))

def set_sprite(type):
    global PLAYER_MOVEMENT_SPRITE_DIMENTION, PLAYER_ACTION_SPRITE_DIMENTION, SCALE, PLAYER_SPRITE_SHEET, DIMENTION, PLAYER, inventory, SHEETS_LIST
    if type == "movement":
        DIMENTION = PLAYER_MOVEMENT_SPRITE_DIMENTION
        SHEET_NUMBER = 0
    elif type == "action" and toolbar.get_selected_item() == "Hoe":
        DIMENTION = PLAYER_MOVEMENT_SPRITE_DIMENTION
        SHEET_NUMBER = 1
    elif type == "action" and toolbar.get_selected_item() == "Water":
        DIMENTION = PLAYER_MOVEMENT_SPRITE_DIMENTION
        SHEET_NUMBER = 2
    PLAYER_SPRITE_SHEET = PlayerSprite(DIMENTION, DIMENTION, SCALE, BLACK)
    PLAYER = PLAYER_SPRITE_SHEET.get_image(SHEETS_LIST[SHEET_NUMBER], PLAYER_SPRITE_MOVEMENT_COL, PLAYER_SPRITE_MOVEMENT_ROW, type, FLIP_CHARACTER)

def can_move_to(x, y):
    global game_map, TILE_X, TILE_Y
    TILE_X = int(x // (game_map.tmx_data.tilewidth * game_map.scale))
    TILE_Y = int(y // (game_map.tmx_data.tileheight * game_map.scale))
    return not game_map.check_collision(TILE_X, TILE_Y)

# Player movement
def player_movement():
    global PLAYER_X, PLAYER_Y, PLAYER_SPRITE_MOVEMENT_ROW, PLAYER_SPRITE_MOVEMENT_COL, FLIP_CHARACTER, DIRECTION, toolbar, inventory, sound_effect_playing, sound
    NEW_X, NEW_Y = PLAYER_X, PLAYER_Y
    
    # SOUND_EFFECT = False

    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP] or keyPressed[pygame.K_w]:
        NEW_Y -= MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 5
        DIRECTION = "u"
        SOUND_EFFECT = True
    elif keyPressed[pygame.K_DOWN] or keyPressed[pygame.K_s]:
        NEW_Y += MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 3
        DIRECTION = "d"
        SOUND_EFFECT = True
    elif keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_a]:
        NEW_X -= MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 4
        FLIP_CHARACTER = True
        DIRECTION = "l"
        SOUND_EFFECT = True
    elif keyPressed[pygame.K_RIGHT] or keyPressed[pygame.K_d]:
        NEW_X += MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 4
        FLIP_CHARACTER = False
        DIRECTION = "r"
        SOUND_EFFECT = True
    elif keyPressed[pygame.K_SPACE]:
        SOUND_EFFECT = False
        if toolbar.get_selected_item() == "Hoe":
            game_map.hoe_land(TILE_X, TILE_Y, DIRECTION)
        elif toolbar.get_selected_item() == "Water":
            game_map.water_land(TILE_X, TILE_Y, DIRECTION)
        elif toolbar.get_selected_item() == "Seed":
            game_map.plant_seed(TILE_X, TILE_Y, DIRECTION, inventory)
    else:
        # Changes character back to standing position
        SOUND_EFFECT = False
        if PLAYER_SPRITE_MOVEMENT_ROW >= 3:
            PLAYER_SPRITE_MOVEMENT_ROW -= 3
    

    if toolbar.get_selected_item() == "Empty" or toolbar.get_selected_item() == "Seed":
        SPRITE = set_sprite("movement")
    else:
        SPRITE = set_sprite("action")

    if can_move_to(NEW_X, PLAYER_Y):
        PLAYER_X = NEW_X
    if can_move_to(PLAYER_X, NEW_Y):
        PLAYER_Y = NEW_Y
    
    # Changes the column by one
    second = pygame.time.get_ticks() / 120
    PLAYER_SPRITE_MOVEMENT_COL = int(second % 6)
    
    
    if SOUND_EFFECT:
        if not sound_effect_playing:
            sound.set_volume(1)
            sound.play(-1)
            sound_effect_playing = True
    else:
        if sound_effect_playing:
            sound.stop()
            sound_effect_playing = False


def main():
    global game_map, OPEN_SHOP, toolbar, PLAYER_SPRITE_SHEET, running, inventory

    # Get item data from ../data/items.json file
    with open('../data/items.json', 'r') as file:
        items_data = json.load(file)
    items_prices = {item['name']: item['price'] for item in items_data['items']}

    # Pygame setup
    init_pygame()

    # Run the prologue first
    # prologue()

    inventory = Inventory()

    set_sprite("movement")

    game = Game(screen)
    game_map = Map("../data/pygame.tmx", SCALE)

    camera = Camera(game_map.width, game_map.height)
    counter = 0
    currency = Currency(INITIAL_CURRENCY, inventory)
    shop = Shop(screen, currency, items_prices)

    toolbar_items = ["Empty", "Hoe", "Water", "Seed"]
    toolbar = Toolbar(toolbar_items)

    while running:
        screen.fill(BLACK)
        game.update()

        # Renders the bottom layer of map
        game_map.render_layers(screen, camera, below_player_layers=[0,1,2,3,5], above_player_layers=[])

        player_rect = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_MOVEMENT_SPRITE_DIMENTION, PLAYER_MOVEMENT_SPRITE_DIMENTION)
        screen.blit(PLAYER, camera.apply(player_rect))
       
        # Renders map elements
        game_map.render_layers(screen, camera, below_player_layers=[], above_player_layers=[4, 6])

        if TILE_X == SHOP_POSE[0] and TILE_Y == SHOP_POSE[1]:
            OPEN_SHOP = True
        if OPEN_SHOP and (pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]):
            OPEN_SHOP = False

        if OPEN_SHOP:
            shop.draw()
        else:
            player_movement()

        camera.update(player_rect)

        # Print texts
        draw_inventory(screen, inventory, font)
        draw_currency(screen, currency, font)
        draw_toolbar(screen, toolbar, font)
        next_day_button = draw_next_day_button(screen)
        
        game_map.expand_land(TILE_X, TILE_Y, DIRECTION, inventory)
        game_map.harvest_crop(TILE_X, TILE_Y, inventory)

        # Allow game to be exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Switch tools using number keys
                if event.key == pygame.K_1:
                    toolbar.select_item(0)
                elif event.key == pygame.K_2:
                    toolbar.select_item(1)
                elif event.key == pygame.K_3:
                    toolbar.select_item(2)
                elif event.key == pygame.K_4:
                    toolbar.select_item(3)

            if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - click_buffer > 400:
                mouse_pos = pygame.mouse.get_pos()
                if next_day_button.collidepoint(mouse_pos):
                    print("next day")
                    game.next_day(game_map)

        pygame.display.flip()
        clock.tick(FPS)  # limits FPS
                
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

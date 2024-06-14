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
PLAYER_ACTION_SPRITE_WIDTH = 48
PLAYER_ACTION_SPRITE_HEIGHT = 48
PLAYER_MOVEMENT_SPRITE_WIDTH = 32
PLAYER_MOVEMENT_SPRITE_HEIGHT = 32
PLAYER_SPRITE_MOVEMENT_ROW_LIST = ["standing_front", "standing_side", "standing_back", "walking_front", "walking_side", "walking_back"]
PLAYER_SPRITE_MOVEMENT_ROW = 0
PLAYER_SPRITE_MOVEMENT_COL = 0
PLAYER_X = 1425
PLAYER_Y = 830
MOVEMENT_SPEED = 2
SCALE = 2.5
FLIP_CHARACTER = True
game_map = None
OPEN_SHOP = False
SHOP_POSE = (35, 18)
TILE_X = 0
TILE_Y = 0
INITIAL_CURRENCY = 100
DIRECTION = "u"

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

def can_move_to(x, y):
    global game_map, TILE_X, TILE_Y
    TILE_X = int(x // (game_map.tmx_data.tilewidth * game_map.scale))
    TILE_Y = int(y // (game_map.tmx_data.tileheight * game_map.scale))
    return not game_map.check_collision(TILE_X, TILE_Y)

# Player movement
def player_movement():
    global PLAYER_X, PLAYER_Y, PLAYER_SPRITE_MOVEMENT_ROW, PLAYER_SPRITE_MOVEMENT_COL, FLIP_CHARACTER, DIRECTION
    NEW_X, NEW_Y = PLAYER_X, PLAYER_Y

    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP]:
        NEW_Y -= MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 5
        DIRECTION = "u"
    elif keyPressed[pygame.K_DOWN]:
        NEW_Y += MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 3
        DIRECTION = "d"
    elif keyPressed[pygame.K_LEFT]:
        NEW_X -= MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 4
        FLIP_CHARACTER = True
        DIRECTION = "l"
    elif keyPressed[pygame.K_RIGHT]:
        NEW_X += MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 4
        FLIP_CHARACTER = False
        DIRECTION = "r"
    else:
        # Changes character back to standing position
        if PLAYER_SPRITE_MOVEMENT_ROW >= 3:
            PLAYER_SPRITE_MOVEMENT_ROW -= 3

    if can_move_to(NEW_X, PLAYER_Y):
        PLAYER_X = NEW_X
    if can_move_to(PLAYER_X, NEW_Y):
        PLAYER_Y = NEW_Y
    
    # Changes the column by one
    second = pygame.time.get_ticks() / 160
    PLAYER_SPRITE_MOVEMENT_COL = int(second % 5)
    
def main():
    global game_map, OPEN_SHOP

    # Get item data from ../data/items.json file
    with open('../data/items.json', 'r') as file:
        items_data = json.load(file)
    items_prices = {item['name']: item['price'] for item in items_data['items']}

    # Pygame setup
    pygame.init()
    pygame.display.set_caption('Title')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont('arial', 40)


    shop = Shop(screen)
    inventory = Inventory()

    player_movement_sprite = pygame.image.load('../assets/images/player/Player.png').convert_alpha()
    player_action_sprite = pygame.image.load("../assets/images/player/Player_Actions.png").convert_alpha()
    player_sprite_sheet = PlayerSprite(player_movement_sprite, player_action_sprite, PLAYER_MOVEMENT_SPRITE_WIDTH, PLAYER_MOVEMENT_SPRITE_HEIGHT, SCALE, BLACK)

    game = Game(screen)
    game_map = Map("../data/pygame.tmx", SCALE)

    camera = Camera(game_map.width, game_map.height)
    counter = 0
    click_buffer = 0
    currency = Currency(INITIAL_CURRENCY,inventory)

    toolbar_items = ["Hoe", "Watering Can", "Axe", "Item"]
    toolbar = Toolbar(toolbar_items)



    while running:
        screen.fill(BLACK)
        game.update()
        game.draw()

        # Renders the bottom layer of map
        game_map.render_layers(screen, camera, below_player_layers=[0,1,2,3, 5], above_player_layers=[])
        # game_map.render_layers(screen, camera, below_player_layers=[1,2], above_player_layers=[])

        player_rect = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_MOVEMENT_SPRITE_WIDTH, PLAYER_MOVEMENT_SPRITE_HEIGHT)
        player = player_sprite_sheet.get_image(PLAYER_SPRITE_MOVEMENT_COL, PLAYER_SPRITE_MOVEMENT_ROW, "movement", FLIP_CHARACTER)
        screen.blit(player,camera.apply(player_rect))
       
        # Renders map elements
        game_map.render_layers(screen, camera, below_player_layers=[], above_player_layers=[ 4, 6])

        if TILE_X == SHOP_POSE[0] and TILE_Y == SHOP_POSE[1]:
            OPEN_SHOP = True
        if OPEN_SHOP and (pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]  ):
            OPEN_SHOP = False

        if OPEN_SHOP:
            if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - click_buffer > 100:
                counter += 1
                click_buffer = pygame.time.get_ticks()
                # mouse_pose = pygame.mouse.get_pos()
                currency.buy(items_prices["dirt"], "dirt")
            shop.draw()
            
        else:
            player_movement()


        camera.update(player_rect)

        # Print texts
        draw_inventory(screen, inventory, font)
        # draw_currency(screen, currency, font)
        # draw_toolbar(screen, toolbar, font)
        
        game_map.change_tile(TILE_X, TILE_Y, DIRECTION)
        
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

        pygame.display.flip()
        clock.tick(FPS)  # limits FPS
                
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# Import libraries
import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, GREEN, BLUE, RED, YELLOW
from game import Game
from playerSprite import PlayerSprite

# Variables
PLAYER_ACTION_SPRITE_WIDTH = 48
PLAYER_ACTION_SPRITE_HEIGHT = 48
PLAYER_MOVEMENT_SPRITE_WIDTH = 32
PLAYER_MOVEMENT_SPRITE_HEIGHT = 32
PLAYER_SPRITE_MOVEMENT_ROW_LIST = ["standing_front", "standing_side", "standing_back", "walking_front", "walking_side", "walking_back"]
PLAYER_SPRITE_MOVEMENT_ROW = 0
PLAYER_SPRITE_MOVEMENT_COL = 0
PLAYER_X = 100
PLAYER_Y = 100
MOVEMENT_SPEED = 1.5
FLIP_CHARACTER = True

# Player movement
def player_movement():
    global PLAYER_X, PLAYER_Y, PLAYER_SPRITE_MOVEMENT_ROW, PLAYER_SPRITE_MOVEMENT_COL, FLIP_CHARACTER
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP]:
        PLAYER_Y -= MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 5
    elif keyPressed[pygame.K_DOWN]:
        PLAYER_Y += MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 3
    elif keyPressed[pygame.K_LEFT]:
        PLAYER_X -= MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 4
        FLIP_CHARACTER = True
    elif keyPressed[pygame.K_RIGHT]:
        PLAYER_X += MOVEMENT_SPEED
        PLAYER_SPRITE_MOVEMENT_ROW = 4
        FLIP_CHARACTER = False
    else:
        # Changes character back to standing position
        if PLAYER_SPRITE_MOVEMENT_ROW >= 3:
            PLAYER_SPRITE_MOVEMENT_ROW -= 3
    
    # Changes the column by one
    second = pygame.time.get_ticks()/200
    PLAYER_SPRITE_MOVEMENT_COL = int(second % 5)

def main():
    # Pygame setup
    pygame.init()
    pygame.display.set_caption('Title')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    player_movement_sprite = pygame.image.load('../assets/images/player/Player.png').convert_alpha()
    player_action_sprite = pygame.image.load("../assets/images/player/Player_Actions.png").convert_alpha()
    player_sprite_sheet = PlayerSprite(player_movement_sprite, player_action_sprite, PLAYER_MOVEMENT_SPRITE_WIDTH, PLAYER_MOVEMENT_SPRITE_HEIGHT, 2, BLACK)

    game = Game(screen)

    while running:
        screen.fill(BLACK)
        game.update()
        game.draw()
        game.draw_text()
        
        player = player_sprite_sheet.get_image(PLAYER_SPRITE_MOVEMENT_COL, PLAYER_SPRITE_MOVEMENT_ROW, "movement", FLIP_CHARACTER)
        screen.blit(player,(PLAYER_X,PLAYER_Y))
        player_movement()
       

        
        
        # Allow game to be exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(FPS)  # limits FPS
                
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
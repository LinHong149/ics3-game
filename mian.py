# Import libraries
import pygame
from plant import plant


# Declare variables
screenWidth = 1280
screenHeight = 800
day = 1
currency = 1000


# Pygame setup
pygame.init()
pygame.display.set_caption('Title')
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True


# Setup text
def updateText():
    global currencyText
    global currencyRect
    font = pygame.font.SysFont('Arial', 32)
    currencyText = font.render(str(currency), True, (0,255,0))
    currencyRect = currencyText.get_rect()
    currencyRect.bottomright = (screenWidth, 32)


# Player movement
def movement(player):
    pygame.draw.rect(screen, (255, 0 ,0), player)
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP]:
        player.move_ip(0, -1)
    elif keyPressed[pygame.K_DOWN]:
        player.move_ip(0, 1)
    elif keyPressed[pygame.K_LEFT]:
        player.move_ip(-1, 0)
    elif keyPressed[pygame.K_RIGHT]:
        player.move_ip(1, 0)


# Declare game elements
player = pygame.Rect((300,250, 30, 30))
# plant1 = plant(stage=1, age=3)


while running:
    # Background
    screen.fill((0,0,0))

    # Player movement
    movement(player)

    # Update and print text
    updateText()
    screen.blit(currencyText, currencyRect)


    clock.tick(60)  # limits FPS to 60

    # Allow game to be exited
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()
            

pygame.quit()
import pygame

class PlayerSprite:
    def __init__(self, width, height, scale, colour):
        self.width = width
        self.height = height
        self.scale = scale
        self.colour = colour

    
    def get_image(self, sheet, frameX, frameY, type, flip):
        self.sheet = sheet

        # image.blit(self.sheet, (0, 0), ((frameX * self.width), (frameY * self.height), self.width, self.height))
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frameX * self.width), (frameY * self.height), self.width, self.width))
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        image = pygame.transform.flip(image, flip, False)
        image.set_colorkey(self.colour)

        return image

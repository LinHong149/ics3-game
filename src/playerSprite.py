import pygame

class PlayerSprite:
    def __init__(self, movement_sheet, action_sheet, width, height, scale, colour):
        self.movement_sheet = movement_sheet
        self.action_sheet = action_sheet
        self.width = width
        self.height = height
        self.scale = scale
        self.colour = colour

    
    def get_image(self, frameX, frameY, type, flip):
        if type == "movement":
            self.sheet = self.movement_sheet
        elif type == "action":
            # frameX *= 2
            # frameY *= 2
            self.sheet = self.action_sheet

        # image.blit(self.sheet, (0, 0), ((frameX * self.width), (frameY * self.height), self.width, self.height))
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frameX * self.width), (frameY * self.height), self.width, self.width))
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        image = pygame.transform.flip(image, flip, False)
        image.set_colorkey(self.colour)

        return image

import pygame 

class Plant:
    def __init__(self, stage:int, age:int, harvest_day:int, value:int):
        self.stage = stage
        self.age = age
        self.harvest_day = harvest_day
        self.value = value

        try:
            self.sheet = pygame.image.load(filename).convert()
        except (pygame.error, message):
            print('Unable to load spritesheet image:', filename)
            raise (SystemExit, message)

    def grow(self, target):
        target.age += 1

    
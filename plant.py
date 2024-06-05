class plant:
    def __init__(self, stage:int, age:int, harvest_day:int, value:int):
        self.stage = stage
        self.age = age
        self.harvest_day = harvest_day
        self.value = value

    def grow(self, target):
        target.age += 1

    
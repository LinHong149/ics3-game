class Currency:
    def __init__(self, initial_amount=0):
        self.amount = initial_amount

    def add(self, amount):
        self.amount += amount

    def subtract(self, amount):
        if self.amount >= amount:
            self.amount -= amount
        else:
            print("Not enough currency!")

    def get_amount(self):
        return self.amount

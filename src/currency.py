class Currency:
    def __init__(self, initial_amount, inventory):
        self.amount = initial_amount
        self.inventory = inventory

    def add(self, amount):
        self.amount += amount

    def buy(self, amount, item):
        if self.amount >= amount:
            self.amount -= amount
            self.inventory.add_item(item)
        else:
            print("Not enough currency!")

    def get_amount(self):
        return self.amount

import pygame

class Currency:
    def __init__(self, amount:int):
        self.amount = amount

    def add(self, amount):
        self.amount += amount

    def subtract(self, price):
        if self.amount - price >= 0:
            self.amount -= price
            return True
        return False

    def get_amount(self):
        return self.amount
        
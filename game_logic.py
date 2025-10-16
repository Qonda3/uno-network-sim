import random

COLORS = ["Red", "Green", "Blue", "Yellow"]
NUMBERS = list(range(0, 10))
ACTIONS = ["Skip", "Reverse", "Draw Two"]
WILDS = ["Wild", "Wild Draw Four"]

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    def __str__(self):
        return f"{self.color} {self.value}" if self.color else self.value
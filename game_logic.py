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
    
class Deck:
    def __init__(self):
        self.cards = []
        for color in COLORS:
            for n in NUMBERS:
                self.cards.append(Card(color, n))
                if n != 0:
                    self.cards.append(Card(color, n))
            for a in ACTIONS:
                self.cards.extend([Card(color, a), Card(color, a)])
        for w in WILDS:
            self.cards.extend([Card(None, w) for _ in range(4)])
        random.shuffle(self.cards)

def draw_card(self):
        if not self.cards:
            raise ValueError("No cards left in the deck")
        return self.cards.pop()

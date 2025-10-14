import random

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    
    def __repr__(self):
        return f"{self.color} {self.value}"
    
def create_deck():
    colors = ['Red', 'Green', 'Blue', 'Yellow']
    values = [str(n) for n in range(0, 10)] + ['Skip', 'Reverse', 'Draw Two']
    deck = [Card(color, value) for color in colors for value in values]

    for _ in range(4):
        deck.append(Card('Wild', 'Wild'))
        deck.append(Card('Wild', 'Draw Four'))
    random.shuffle(deck)
    return deck